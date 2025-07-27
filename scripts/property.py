from homeharvest import scrape_property
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

'''
TODO: Cache results from New Mexico neighborhoods, city, state, and zip code
lookups to avoid repeated API calls.
'''

# Load FHFA HPI state-level data which contains historical home price indices
hpi = pd.read_csv(
    "./hpi_po_state.txt", sep='\t',
    dtype={'state': str, 'yr': int, 'qtr': int, 'index_sa': float}
)
hpi = hpi[['state', 'yr', 'qtr', 'index_sa']]
hpi['quarter_date'] = pd.PeriodIndex.from_fields(
    year=hpi['yr'], quarter=hpi['qtr'], freq='Q').to_timestamp(how='end')
hpi_index = hpi.set_index(['state', 'quarter_date'])['index_sa'].sort_index()
latest_hpi = hpi.sort_values('quarter_date').groupby('state')['index_sa'].last()

def normalize_string(s):
    return s.strip().lower() if isinstance(s, str) else ""

def filter_exact_address(df, street):
    if df is None or df.empty:
        return pd.DataFrame()

    # Normalize the street address for a more precise match
    target_street = normalize_string(street)
    return df[df['street'].apply(normalize_string) == target_street]

def inflation_index_lookup(state: str, date: pd.Timestamp) -> float:
    """
    Returns the inflation index ratio to convert past prices to present-day
    equivalents using FHFA HPI for the given state and date.
    """
    # Convert sale date to the start of its quarter for lookup
    quarter_start = pd.to_datetime(date).to_period('Q').to_timestamp()

    try:
        past_index = hpi_index.loc[(state, quarter_start)]
        current_index = latest_hpi[state]
        # Calculate the inflation multiplier
        return current_index / past_index
    except KeyError:
        # If the index is not found (e.g., missing data), return 1.0 to indicate no change
        return 1.0

def get_price_series(df):
    """
    Returns the most reliable price series from the DataFrame, with
    inflation-adjusted last_sold_price (only if last_sold_date < cutoff_years old),
    using FHFA HPI for the appropriate state.
    """
    # Define the cutoff date for filtering
    cutoff_years = 10
    cutoff_date = datetime.now() - timedelta(days=cutoff_years * 365.25)

    # Price priority: sold price > list price > last sold price > estimated value
    # 1. Sold Price
    if 'sold_price' in df.columns and not df['sold_price'].dropna().empty:
        return df['sold_price'].dropna().astype(float)

    # 2. List Price
    if 'list_price' in df.columns and not df['list_price'].dropna().empty:
        return df['list_price'].dropna().astype(float)

    # 3. Last Sold Price (if recent and adjustable)
    if {'last_sold_price', 'last_sold_date', 'state'}.issubset(df.columns):
        # Filter for recent sales with valid dates and prices
        recent_sales = df[
            (pd.to_datetime(df['last_sold_date'], errors='coerce') >
             cutoff_date) &
            (df['last_sold_price'].notna())
        ].copy()

        if not recent_sales.empty:
            # Apply inflation adjustment
            inflation_multiplier = recent_sales.apply(
                lambda row: inflation_index_lookup(row['state'], row['last_sold_date']),
                axis=1
            )
            adjusted_prices = recent_sales['last_sold_price'] * inflation_multiplier
            return adjusted_prices.dropna().astype(float)

    # 4. Estimated Value (fallback)
    if 'estimated_value' in df.columns and not df['estimated_value'].dropna().empty:
        return df['estimated_value'].dropna().astype(float)

    # Return an empty Series if no prices are found
    return pd.Series(dtype='float64')

def inspect_results(result, address: str):
    if result is None or result.empty:
        print(f"No properties found for location: {address}")
        return

    print(f"\nFound {len(result)} properties for {address}.\n")

    # Show basic info with available prices
    for idx, row in result.iterrows():
        address = row.get('street', 'N/A')
        city = row.get('city', '')
        zip_code = row.get('zip_code', '')
        state = row.get('state', '')
        sold = row.get('sold_price', '—')
        listp = row.get('list_price', '—')
        last_sold = row.get('last_sold_price', '—')
        est = row.get('estimated_value', '—')

        print(f"{idx + 1}. {address}, {city}, {zip_code}, {state}")
        print(f"   List: {listp} | Sold: {sold} | Last Sold: {last_sold} |"
          " Estimate: {est}")

def get_property_value(location: str, location_type: str, property_data=None):
    """Helper function to scrape and calculate average property value."""
    if property_data is None:
        try:
            property_data = scrape_property(location=location)
        except Exception as e:
            print(f"Failed to scrape property data for {location}: {e}")
            return None

    if property_data.empty:
        return None

    # inspect_results(property_data, location) # for debugging

    # Filter based on location type
    if location_type == 'zip':
        filtered_data = property_data[property_data['zip_code'].astype(str) == str(location)]
    elif location_type == 'city':
        filtered_data = property_data[property_data['city'].str.lower() == location.lower()]
    elif location_type == 'state':
        filtered_data = property_data[property_data['state'].str.lower() == location.lower()]
    elif location_type == 'neighborhood':
        if 'neighborhoods' in property_data.columns:
            # Filter by checking if the neighborhood string is contained in the 'neighborhoods' column
            # This handles cases where the column might contain multiple neighborhoods or broader areas
            filtered_data = property_data[property_data['neighborhoods'].str.contains(location, case=False, na=False)]
        else:
            print(f"Warning: 'neighborhoods' column not found in scraped data for {location}. Using all data.")
            filtered_data = property_data
    else:
        filtered_data = property_data

    prices = get_price_series(filtered_data)
    if prices.empty:
        return None

    MIN_PRICE_BOUND = 10000
    MAX_PRICE_BOUND = 50000000

    # Apply absolute price bounds
    filtered_prices = prices[(prices >= MIN_PRICE_BOUND) & (prices <= MAX_PRICE_BOUND)]

    original_count = len(prices)
    filtered_count = len(filtered_prices)

    if original_count > filtered_count:
        num_filtered = original_count - filtered_count
        '''
        print(f"Warning: Filtered out {num_filtered} "
              f"({num_filtered/original_count:.1%}) property values as "
              f"outliers (below ${lower_bound:,.2f} or above "
              f"${upper_bound:,.2f}) for {location}: "
              f"{', '.join(map(lambda x: f"${x:,.2f}", outliers.tolist()))}.")
        '''

    mean = filtered_prices.mean() if not filtered_prices.empty else None
    median = filtered_prices.median() if not filtered_prices.empty else None
    return mean, median, filtered_count

def estimate_property_value(street: str, city: str, state: str, zip_code: str):
    if street is None:
        address = f"{city}, {state}"
    else:
        address = f"{street}, {city}, {state} {zip_code}"

    # Option 1: Exact address match
    try:
        property_data = scrape_property(location=address)
        exact_match = filter_exact_address(property_data, street)
        exact_prices = get_price_series(exact_match)
        if not exact_prices.empty:
            value = exact_prices.iloc[0]
            print(f"Exact match found for ${address}. Estimated value: ${value:,.2f}")
            return value, value
    except Exception as e:
        print(f"Failed to scrape property data for {address}: {e}")

    # Option 2: Radius-level average
    radius = 1  # miles
    try:
        property_data_radius = scrape_property(location=address, radius=radius)
        if not property_data_radius.empty:
            # Use get_property_value to apply outlier filtering
            mean, median = get_property_value(
                address, 'radius', property_data=property_data_radius)
            if mean:
                print(f"No exact match for {address}. Using {radius}-mile radius average: "
                      f"${mean:,.2f}")
                return mean, median
    except Exception as e:
        print(f"Failed to scrape property data for {address} with radius: {str(e)}")

    # Option 3: ZIP-level average
    mean, median = get_property_value(zip_code, 'zip')
    if mean:
        print(f"No radius match for {address}. Using ZIP Code average: ${mean:,.2f}")
        return mean, median

    # Option 4: City-level average
    mean, median = get_property_value(city, 'city')
    if mean:
        print(f"No ZIP match for {address}. Using city-wide average: ${mean:,.2f}")
        return mean, median

    # Option 5: State-level average
    mean, median = get_property_value(state, 'state')
    if mean:
        print(f"No city match for {address}. Using state-wide average: "
              f"${mean:,.2f}")
        return mean, median

    print(f"No matching properties found in address, ZIP, city, or state for ${address}.")
    return None

def run_tests():
    """
    Test cases with preliminary expected values.
    """
    test_cases = [
        {
            "name": "Anytown, CA",
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "90210",
            "expected": 5601000  # Replace with your expected value
        },
        {
            "name": "Albuquerque, NM (1)",
            "street": "123 Main St NE",
            "city": "Albuquerque",
            "state": "NM",
            "zip_code": "87102",
            "expected": 349000  # Replace with your expected value
        },
        {
            "name": "Alexandria, VA",
            "street": "6731 Williams Dr",
            "city": "Alexandria",
            "state": "VA",
            "zip_code": "22307",
            "expected": 527000  # Replace with your expected value
        },
        {
            "name": "Albuquerque, NM (2)",
            "street": "5728 Del Frate Pl NW",
            "city": "Albuquerque",
            "state": "NM",
            "zip_code": "87105",
            "expected": 299000  # Replace with your expected value
        },
        {
            "name": "Albuquerque, NM (3)",
            "street": "1036 Red Oaks Loop NE",
            "city": "Albuquerque",
            "state": "NM",
            "zip_code": "87122",
            "expected": 797000  # Replace with your expected value
        }
    ]

    print("Running property value estimation tests...")
    for test in test_cases:
        print(f"--- Running Test: {test['name']} ---")
        estimated_mean_value, estimated_median_value = estimate_property_value(
            street=test["street"],
            city=test["city"],
            state=test["state"],
            zip_code=test["zip_code"]
        )
        
        if estimated_mean_value is not None or estimated_median_value is not None:
            print(f"Expected: ${test['expected']:,.2f}")
            print(f"Estimated mean: ${estimated_mean_value:,.2f}; "
                  f"Estimated median: ${estimated_median_value:,.2f}")
            error_tolerance = 0.10 * test['expected']
            if abs(estimated_mean_value - test['expected']) < error_tolerance:
                print("Result: PASS\n")
            else:
                print("Result: FAIL\n")
        else:
            print("Result: FAIL (No value estimated)\n")

def analyze_abq_neighborhoods(file_path="AbqNeighborhoods.txt"):
    """
    Reads a list of Albuquerque neighborhoods, scrapes property data for each,
    and calculates the mean and median property values.
    """
    print(f"\nAnalyzing Albuquerque neighborhoods from {file_path}...")
    results = []
    try:
        with open(file_path, 'r') as f:
            print(f"Neighborhood	Mean	Median", flush=True)
            for line in f:
                neighborhood = line.strip()
                if neighborhood:
                    # scrape_property often treats neighborhood as part of city context
                    location = f"{neighborhood}"
                    property_data = scrape_property(location=location)
                    mean_median_tuple = get_property_value(location, 'neighborhood', property_data)
                    if mean_median_tuple is None:
                        mean_val, median_val = None, None
                    else:
                        mean_val, median_val = mean_median_tuple

                    # Format mean_val and median_val for printing, handling None
                    neighborhood_str = f"{neighborhood}"
                    mean_str = f"{mean_val:,.2f}" if mean_val is not None else "N/A"
                    median_str = f"{median_val:,.2f}" if median_val is not None else "N/A"

                    print(f"{neighborhood_str}	{mean_str}	{median_str}", flush=True)

    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

if __name__ == "__main__":
    run_tests()
    # analyze_abq_neighborhoods()
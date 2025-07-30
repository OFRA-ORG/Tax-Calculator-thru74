import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


def analyze_similarity_cosine(db_path, household_id, top_n=10):
    """
    Analyzes tax reform impact by identifying similar households.

    Args:
        db_path (str): The path to the SQLite database file.
        household_id (int): The ID of the household to analyze.
        top_n (int): The number of similar households to return.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    # Connect to the database
    con = sqlite3.connect(db_path)

    # Read the base, baseline and reform data
    base_df = pd.read_sql_query("SELECT * FROM base", con)
    baseline_df = pd.read_sql_query("SELECT * FROM baseline", con)
    reform_df = pd.read_sql_query("SELECT * FROM reform", con)

    # Merge all three dataframes
    merged_df = pd.merge(base_df, baseline_df, on="RECID")
    merged_df = pd.merge(
        merged_df, reform_df, on="RECID", suffixes=("_baseline", "_reform")
    )

    # Calculate the tax change
    merged_df["tax_change"] = (
        merged_df["combined_reform"] - merged_df["combined_baseline"]
    )

    # Select the features for similarity analysis based on feature importance
    features = [
        # Wages, salaries, and tips for filing unit net of pension contributions
        "e00200_baseline",
        # Net long-term capital gains/losses
        "p23250_baseline",
        # Age in years of taxpayer
        "age_head",
        # Sch C business net profit/loss for filing unit
        "e00900_baseline",
        # Number of EIC qualifying children
        "EIC_baseline",
        # Number of children who are Child-Tax-Credit eligible, one condition for which is being under age 17
        "n24_baseline",
        # Filing (marital) status:
        "MARS",
        # Total number of exemptions for filing unit
        "XTOT",
    ]

    # Create a DataFrame with the selected features, handle missing columns,
    # convert to numeric, and scale to normalize the values
    feature_df = (
        merged_df.set_index("RECID")[features]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
    )
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_df)
    scaled_feature_df = pd.DataFrame(
        scaled_features, index=feature_df.index, columns=feature_df.columns
    )

    # Calculate the cosine similarity
    target_household_features = scaled_feature_df.loc[[household_id]]
    similarity_scores = cosine_similarity(
        target_household_features, scaled_feature_df
    )[0]

    # Create series of similarity scores and return top N similar households
    similarity_series = pd.Series(
        similarity_scores, index=scaled_feature_df.index
    )
    similar_households = similarity_series.sort_values(ascending=False)
    top_similar_households = similar_households.iloc[1 : top_n + 1]

    # Calculate average tax change for top similar households
    similar_households_tax_change = merged_df[
        merged_df["RECID"].isin(top_similar_households.index)
    ]["tax_change"]
    average_tax_change = similar_households_tax_change.mean()

    # Get the data for the specified household
    household_data = merged_df[merged_df["RECID"] == household_id]

    return {
        "household_id": household_id,
        "household_data": household_data.to_dict("records")[0],
        "similar_households": top_similar_households.to_dict(),
        "average_tax_change_for_similar_households": average_tax_change,
    }


def analyze_similarity_cluster_features(
    db_path, household_id, tolerance_percent=0.20
):
    """
    Analyzes tax reform impact by identifying similar households based on
    features important for clustering.

    Args:
        db_path (str): Path to the SQLite database file.
        household_id (int): ID of the household to analyze.
        tolerance_percent (float): Percentage tolerance for numerical features.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    # Connect to the database
    con = sqlite3.connect(db_path)

    # Read the base, baseline and reform data and merge them
    base_df = pd.read_sql_query("SELECT * FROM base", con)
    baseline_df = pd.read_sql_query("SELECT * FROM baseline", con)
    reform_df = pd.read_sql_query("SELECT * FROM reform", con)
    merged_df = pd.merge(base_df, baseline_df, on="RECID")
    merged_df = pd.merge(
        merged_df, reform_df, on="RECID", suffixes=("_baseline", "_reform")
    )

    # Calculate the tax change
    merged_df["tax_change"] = (
        merged_df["combined_reform"] - merged_df["combined_baseline"]
    )

    # Features identified as important for clustering
    # Categorical/Discrete features for exact match
    categorical_features = ["MARS", "XTOT"]
    # Numerical features for percentage-based similarity
    numerical_features = [
        "age_head_baseline",
        "n24_baseline",
        "EIC_baseline",
        "expanded_income",
        "e00200_baseline",
        "c04470_baseline",
    ]

    # Get the target household's data
    household_data = merged_df[merged_df["RECID"] == household_id]
    target_household_data = household_data.iloc[0]

    # Initialize a boolean series for filtering, all True initially
    similar_mask = pd.Series(True, index=merged_df.index)

    # Apply filters for categorical features (exact match)
    for feature in categorical_features:
        if feature in target_household_data and feature in merged_df.columns:
            similar_mask &= merged_df[feature] == target_household_data[feature]

    # Apply filters for numerical features (within tolerance)
    for feature in numerical_features:
        if feature in target_household_data and feature in merged_df.columns:
            target_value = target_household_data[feature]
            if target_value != 0:  # Avoid division by zero for percentage
                lower_bound = target_value * (1 - tolerance_percent)
                upper_bound = target_value * (1 + tolerance_percent)
                similar_mask &= (merged_df[feature] >= lower_bound) & (
                    merged_df[feature] <= upper_bound
                )
            else:  # If target value is 0, only exact matches are similar
                similar_mask &= merged_df[feature] == 0

    # Filter out the target household itself
    similar_mask &= merged_df["RECID"] != household_id

    # Get the similar households based on the mask
    similar_households_df = merged_df[similar_mask].copy()

    if not similar_households_df.empty:
        top_similar_households = similar_households_df["RECID"]
    else:
        top_similar_households = pd.Series(dtype="int64")  # Empty Series

    # Get the tax change for the top similar households
    similar_households_tax_change = merged_df[
        merged_df["RECID"].isin(top_similar_households.tolist())
    ]["tax_change"]

    # Calculate the average tax change for the similar households
    average_tax_change = (
        similar_households_tax_change.mean()
        if not similar_households_tax_change.empty
        else None
    )

    return {
        "household_id": household_id,
        "household_data": household_data.to_dict("records")[0],
        "similar_households": top_similar_households.to_dict(),
        "average_tax_change_for_similar_households": average_tax_change,
    }


if __name__ == "__main__":
    # Specify the paths to the databases
    db_path = "tmd_nm-26-#-ext-#.dumpdb"
    household_ids_to_analyze = [3, 10, 100, 1000, 10000]

    print(f"ID\tTax change\tCosine top 10 similar\tCluster similar")
    for hh in household_ids_to_analyze:
        analysis_results_cosine = analyze_similarity_cosine(db_path, hh)
        analysis_results_cluster = analyze_similarity_cluster_features(
            db_path, hh
        )
        print(f"{hh}\t${analysis_results_cosine['household_data']['tax_change']:.2f}\t"
              f"${analysis_results_cosine['average_tax_change_for_similar_households']:.2f} "
              f"(n={len(analysis_results_cosine['similar_households'])})\t"
              f"${analysis_results_cluster['average_tax_change_for_similar_households']:.2f} "
              f"(n={len(analysis_results_cluster['similar_households'])})")
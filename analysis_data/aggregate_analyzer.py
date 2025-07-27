import sqlite3
import pandas as pd

def analyze_aggregates(db_path):
    """
    Analyzes the aggregate tax change for a given database.

    Args:
        db_path (str): The path to the SQLite database file.

    Returns:
        float: The total aggregate tax change for the region.
    """
    # Connect to the database
    con = sqlite3.connect(db_path)

    # Read the base, baseline and reform data
    base_df = pd.read_sql_query("SELECT RECID, s006 FROM base", con) # Only need RECID and s006 from base
    baseline_df = pd.read_sql_query("SELECT RECID, combined FROM baseline", con)
    reform_df = pd.read_sql_query("SELECT RECID, combined FROM reform", con)

    # Merge all three dataframes
    merged_df = pd.merge(base_df, baseline_df, on="RECID")
    merged_df = pd.merge(merged_df, reform_df, on="RECID", suffixes=("_baseline", "_reform"))

    # Calculate the tax change for each household
    merged_df["tax_change"] = merged_df["combined_reform"] - merged_df["combined_baseline"]

    # Calculate the weighted aggregate tax change
    # s006 is the sampling weight
    aggregate_tax_change = (merged_df["tax_change"] * merged_df["s006"]).sum()

    return aggregate_tax_change

if __name__ == "__main__":
    # Specify the paths to the databases
    db_paths = [
        "tmd_nm-26-#-ext-#.dumpdb",
        "tmd_nm01-26-#-ext-#.dumpdb",
        "tmd_nm02-26-#-ext-#.dumpdb",
        "tmd_nm03-26-#-ext-#.dumpdb"
    ]

    print("\n--- Aggregate Tax Change Analysis ---")
    for db_path in db_paths:
        aggregate_change = analyze_aggregates(db_path)
        print(f"  - {db_path}: ${aggregate_change:,.2f}")


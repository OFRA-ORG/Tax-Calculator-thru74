import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def analyze_features(db_path):
    """
    Analyzes the features in the database to determine which are most predictive of tax change.

    Args:
        db_path (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing two pandas Series:
               - The top correlated features.
               - The top features from the Random Forest model.
    """
    # Connect to the database
    con = sqlite3.connect(db_path)

    # Read the base, baseline and reform data
    base_df = pd.read_sql_query("SELECT * FROM base", con)
    baseline_df = pd.read_sql_query("SELECT * FROM baseline", con)
    reform_df = pd.read_sql_query("SELECT * FROM reform", con)

    # Merge all three dataframes
    merged_df = pd.merge(base_df, baseline_df, on="RECID")
    merged_df = pd.merge(merged_df, reform_df, on="RECID", suffixes=("_baseline", "_reform"))

    # Calculate the tax change
    merged_df["tax_change"] = merged_df["combined_reform"] - merged_df["combined_baseline"]

    # --- Correlation Analysis ---
    # Select only numeric columns for correlation analysis
    numeric_df = merged_df.apply(pd.to_numeric, errors='coerce')
    numeric_df = numeric_df.dropna(axis=1, how='all') # drop columns that are all NaN
    
    # Calculate the correlation with the tax_change column
    correlations = numeric_df.corr()["tax_change"].abs().sort_values(ascending=False)

    # --- Random Forest Feature Importance ---
    # Define the features (X) and the target (y)
    # Use only baseline features for X, and ensure they are present in the merged_df
    feature_cols = [
        "iitax",
        "combined",
        "c04470",
        "e00200",
        "p23250",
        "age_head",
        "e00900",
        "EIC",
        "n24",
        "MARS", 
        "expanded_income", 
        "XTOT" 
    ]
    # Append '_baseline' to features that come from the baseline table
    X_cols = [f'{col}_baseline' for col in feature_cols if col not in ["MARS", "expanded_income", "XTOT"]]
    X_cols.extend([col for col in feature_cols if col in ["MARS", "expanded_income", "XTOT"]])

    X = merged_df[X_cols].fillna(0) # fill NaNs with 0 for the model
    y = merged_df["tax_change"].fillna(0)

    # Initialize and train the Random Forest model
    model = RandomForestRegressor(random_state=42, n_jobs=-1)
    model.fit(X, y)

    # Get the feature importances
    feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

    return correlations, feature_importances

if __name__ == "__main__":
    # Specify the path to the database
    db_path = "tmd_nm-26-#-ext-#.dumpdb" # Only analyze the state-level database

    print(f"\n=====================================================")
    print(f"Analyzing features for database: {db_path}")
    print(f"=====================================================")
    correlations, feature_importances = analyze_features(db_path)

    # --- Output ---
    print("\n--- Top 15 Features by Correlation with Tax Change ---")
    print(correlations.head(15))
    print("\n--- Top 15 Features by Random Forest Importance ---")
    print(feature_importances.head(15))
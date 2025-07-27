import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def analyze_clusters(db_path, n_clusters=4):
    """
    Performs clustering analysis on household data to identify similar groups
    and determines feature importance for distinguishing these groups.

    Args:
        db_path (str): The path to the SQLite database file.
        n_clusters (int): The number of clusters for KMeans.

    Returns:
        tuple: A tuple containing:
               - pandas DataFrame: Centroids of the clusters.
               - pandas Series: Feature importances for distinguishing clusters.
    """
    # Connect to the database
    con = sqlite3.connect(db_path)

    # Read the base, baseline and reform data
    base_df = pd.read_sql_query("SELECT * FROM base", con)
    baseline_df = pd.read_sql_query("SELECT * FROM baseline", con)
    reform_df = pd.read_sql_query("SELECT * FROM reform", con)

    print("Base DF Columns:", base_df.columns.tolist())
    print("Baseline DF Columns:", baseline_df.columns.tolist())
    print("Reform DF Columns:", reform_df.columns.tolist())

    # Merge all three dataframes
    merged_df = pd.merge(base_df, baseline_df, on="RECID")
    merged_df = pd.merge(merged_df, reform_df, on="RECID",
                         suffixes=("_baseline", "_reform"))

    # Define features for clustering (household characteristics)
    # These are chosen to represent different aspects of a household's finances
    # and demographics.
    features_for_clustering = [
        "expanded_income",  # Total income
        "MARS",             # Marital status
        "XTOT",             # Number of exemptions (family size proxy)
        "e00200_baseline",  # Wage and salary income
        "c04470_baseline",  # Itemized deductions
        "age_head_baseline",# Age of household head
        "EIC_baseline",     # Earned Income Credit amount
        "n24_baseline"      # Number of children under 24
    ]

    # Prepare the data for clustering
    # Use only baseline features for X, and ensure they are present
    X_clustering = merged_df[features_for_clustering].copy()
    X_clustering = X_clustering.fillna(0) # Fill NaNs with 0 for clustering

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clustering)
    X_scaled_df = pd.DataFrame(X_scaled, columns=features_for_clustering)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    merged_df['cluster_label'] = kmeans.fit_predict(X_scaled_df)

    # Analyze cluster characteristics (centroids)
    # Inverse transform centroids to original scale for interpretability
    cluster_centers_scaled = kmeans.cluster_centers_
    cluster_centers_original_scale = scaler.inverse_transform(
        cluster_centers_scaled)
    cluster_centroids_df = pd.DataFrame(
        cluster_centers_original_scale,
        columns=features_for_clustering
    )
    cluster_centroids_df.index.name = 'Cluster'

    # Determine feature importance for distinguishing clusters
    # Train a RandomForestClassifier to predict cluster labels
    clf = RandomForestClassifier(random_state=42, n_jobs=-1)
    clf.fit(X_scaled_df, merged_df['cluster_label'])
    feature_importances = pd.Series(
        clf.feature_importances_,
        index=features_for_clustering
    ).sort_values(ascending=False)

    return cluster_centroids_df, feature_importances

if __name__ == "__main__":
    db_path = "tmd_nm-26-#-ext-#.dumpdb" # Path relative to this script

    print(f"\n=====================================================")
    print(f"Performing clustering analysis for database: {db_path}")
    print(f"=====================================================")

    cluster_centroids, cluster_feature_importances = analyze_clusters(db_path)

    print("\n--- Cluster Centroids (Average Feature Values per Cluster) ---")
    print(cluster_centroids.round(2))

    print("\n--- Feature Importance for Distinguishing Clusters ---")
    print(cluster_feature_importances.head(10))


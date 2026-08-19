"""
====================================================================================================
MODULE: cleaning.py
====================================================================================================
Performs robust in-memory data hygiene, bot/QA filtering, deduplication, and anomaly capping.
====================================================================================================
"""

import pandas as pd
import numpy as np

def clean_retail_panel(df_panel):
    """Cleans retail panel transactions: deduplicates, removes extreme 120x spikes and negative prices."""
    df_clean = df_panel.drop_duplicates().copy()
    df_clean["units_sold"] = pd.to_numeric(df_clean["units_sold"], errors="coerce").fillna(0)
    df_clean = df_clean[(df_clean["units_sold"] > 0) & (df_clean["units_sold"] < 3000)]
    return df_clean

def clean_audience_signal(df_aud):
    """Filters bot crawlers, scrapers, internal QA accounts, and invalid duration sessions."""
    df_clean = df_aud.drop_duplicates().copy()
    
    # Identify bot traffic
    bot_mask = df_clean["user_id"].str.startswith("BOT_", na=False) | df_clean["device_type"].isin([
        "HeadlessChrome", "Datadog-Synthetics", "Python-urllib/3.10", "Android_Emulator_0x0"
    ])
    
    # Identify internal QA accounts
    qa_mask = df_clean["campaign_tag"].str.contains("Summer_Nitro_Blitz", na=False) | df_clean["user_id"].str.startswith("QA_", na=False)
    
    df_clean = df_clean[~bot_mask & ~qa_mask]
    df_clean = df_clean[df_clean["session_duration_seconds"] >= 0]
    df_clean = df_clean[df_clean["engagement_clicks"] < 100000]
    return df_clean

def clean_distribution_audit(df_dist_audit):
    """Aggregates distribution audits across 24 months and caps impossible stocking counts."""
    dist_summary = df_dist_audit.groupby("District_Num_ID").agg(
        Avg_Kestrel_Stocking=("Outlets_Stocking_Kestrel", "mean"),
        Avg_Category_Stocking=("Outlets_Stocking_Category", "mean"),
        Universe=("Estimated_Total_Universe", "mean")
    ).reset_index()

    # Cap stocking at total universe
    dist_summary["Avg_Category_Stocking_Clean"] = np.minimum(
        dist_summary["Avg_Category_Stocking"], dist_summary["Universe"]
    )
    dist_summary["Avg_Kestrel_Stocking_Clean"] = np.minimum(
        dist_summary["Avg_Kestrel_Stocking"], dist_summary["Avg_Category_Stocking_Clean"]
    )
    
    # Distribution Gap = 1 - (Outlets Stocking Kestrel / Outlets Stocking Category)
    cat_stocking_safe = np.maximum(dist_summary["Avg_Category_Stocking_Clean"], 1.0)
    dist_summary["distribution_gap"] = (
        1.0 - (dist_summary["Avg_Kestrel_Stocking_Clean"] / cat_stocking_safe)
    ).clip(0.0, 1.0).round(4)
    
    return dist_summary

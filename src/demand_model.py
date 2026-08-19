"""
====================================================================================================
MODULE: demand_model.py
====================================================================================================
Constructs the independent consumer demand signal strictly excluding Kestrel sales.
Normalizes for population disparity and computes percentile ranks.
====================================================================================================
"""

import numpy as np
import pandas as pd

def build_independent_demand_signal(df_master, df_panel_clean, df_aud_clean):
    """
    Constructs the composite independent demand signal (0.0 to 1.0) from 4 independent sources:
      1. Category Shelf Velocity in Retail Panel (45%)
      2. Audience Telemetry Events (25%)
      3. Campus Music/Sports Event Registrations (20%)
      4. Search Volume Queries (10%)
    """
    # 1. Category Velocity (all brands excluding Kestrel)
    cat_velocity = df_panel_clean.groupby("District_Num_ID")["units_sold"].agg(
        Total_Category_Units=("sum"),
        Avg_Units_Per_Audit=("mean"),
        Audit_Count=("count")
    ).reset_index()
    
    # 2. Audience Telemetry Aggregations
    aud_agg = df_aud_clean.groupby("District_Num_ID").agg(
        Total_Audience_Events=("event_id", "count"),
        Total_Engagement_Clicks=("engagement_clicks", "sum"),
        Campus_Registrations=("event_type", lambda x: (x == "campus_event_registration").sum()),
        Search_Queries=("event_type", lambda x: (x == "search_query").sum())
    ).reset_index()
    
    # Merge with Master
    merged = df_master.merge(cat_velocity, on="District_Num_ID", how="left").fillna(0)
    merged = merged.merge(aud_agg, on="District_Num_ID", how="left").fillna(0)
    
    # Population normalization (per 100,000 residents) to prevent big-city bias
    pop_100k = np.maximum(merged["Total_Population"] / 100000.0, 1.0)
    merged["Audience_Events_Per_100k"] = merged["Total_Audience_Events"] / pop_100k
    merged["Campus_Registrations_Per_100k"] = merged["Campus_Registrations"] / pop_100k
    merged["Search_Queries_Per_100k"] = merged["Search_Queries"] / pop_100k
    
    # Percentile-Rank Scaling
    r_vel = merged["Avg_Units_Per_Audit"].rank(pct=True)
    r_aud = merged["Audience_Events_Per_100k"].rank(pct=True)
    r_cam = merged["Campus_Registrations_Per_100k"].rank(pct=True)
    r_sch = merged["Search_Queries_Per_100k"].rank(pct=True)
    
    merged["demand_signal"] = (
        0.45 * r_vel +
        0.25 * r_aud +
        0.20 * r_cam +
        0.10 * r_sch
    ).clip(0.0, 1.0).round(4)
    
    return merged

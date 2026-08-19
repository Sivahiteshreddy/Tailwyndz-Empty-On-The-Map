"""
====================================================================================================
MODULE: opportunity_sizing.py
====================================================================================================
Sizes the annual incremental revenue potential in INR (₹ Crores) for shortlisted markets.
====================================================================================================
"""

import pandas as pd
import numpy as np

def size_market_opportunities(df_master, net_price_per_can=85.0, target_share=0.28):
    """
    Estimates annual incremental revenue potential in INR (₹ Crores):
      Annual Category Cans = Universe * Category Stocking % * Velocity * 12
      Opportunity INR = Category Cans * Distribution Gap * Target Share (28%) * Net Can Price (₹85)
    """
    df_qualified = df_master[
        df_master["Classification"] == "Likely Expansion Opportunity"
    ].sort_values("WCI", ascending=False).copy()
    
    df_qualified["Estimated_Annual_Category_Cans"] = (
        df_qualified["Estimated_Total_Retail_Universe"] *
        (df_qualified["Avg_Category_Stocking_Clean"] / np.maximum(df_qualified["Estimated_Total_Retail_Universe"], 1.0)) *
        df_qualified["Avg_Units_Per_Audit"] * 12.0
    )
    
    df_qualified["Annual_Opportunity_INR"] = (
        df_qualified["Estimated_Annual_Category_Cans"] *
        df_qualified["distribution_gap"] *
        target_share *
        net_price_per_can
    )
    df_qualified["Annual_Opportunity_Cr"] = (df_qualified["Annual_Opportunity_INR"] / 10000000.0).round(2)
    
    interventions = [
        "Distribution Expansion & Chiller Placement",
        "Distribution Expansion & Campus Sampling",
        "Distribution Expansion (D2C & Quick Commerce)",
        "Distribution Expansion & Modern Trade Listing",
        "Distribution Expansion & Retailer Margin Incentive"
    ]
    
    top5 = df_qualified.head(5).copy()
    top5["Recommended_Intervention"] = interventions[:len(top5)]
    return df_qualified, top5

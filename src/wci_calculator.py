"""
====================================================================================================
MODULE: wci_calculator.py
====================================================================================================
Calculates Competitive Intensity, Whitespace Confidence Index (WCI), and classifies districts.
====================================================================================================
"""

import pandas as pd
import numpy as np

def calculate_competitive_intensity(df_panel_clean):
    """Calculates the share of category volume held by the top two rival brands per district."""
    comp_vols = df_panel_clean[df_panel_clean["brand"] != "Kestrel"].groupby(
        ["District_Num_ID", "brand"]
    )["units_sold"].sum().unstack().fillna(0)
    
    total_cat_vol = df_panel_clean.groupby("District_Num_ID")["units_sold"].sum()
    top2_vol = comp_vols.apply(lambda row: row.nlargest(2).sum(), axis=1)
    
    comp_intensity = (top2_vol / total_cat_vol).clip(0.0, 1.0).round(4)
    return pd.DataFrame({"District_Num_ID": comp_intensity.index, "competitive_intensity": comp_intensity.values})

def compute_wci_and_classify(df_master):
    """
    Computes Whitespace Confidence Index (WCI) using exact formula:
      WCI = 0.45 * demand_signal + 0.35 * distribution_gap + 0.20 * (1 - competitive_intensity)
    
    Applies strategic classification rules.
    """
    df_master["WCI"] = (
        0.45 * df_master["demand_signal"] +
        0.35 * df_master["distribution_gap"] +
        0.20 * (1.0 - df_master["competitive_intensity"])
    ).round(4)
    
    def classify(row):
        cov = row["Mean_Panel_Coverage_Pct"]
        wci = row["WCI"]
        dist_gap = row["distribution_gap"]
        demand = row["demand_signal"]
        comp_int = row["competitive_intensity"]
        
        # 1. Low Coverage / Panel Blindness Filter (<60%)
        if cov < 60.0:
            return "UNKNOWN (Panel Blindness / Low Sampling)"
        
        # 2. Qualified Whitespace Opportunity
        if wci >= 0.70 and dist_gap >= 0.40 and comp_int < 0.80:
            return "Likely Expansion Opportunity"
        
        # 3. Competitive Lockout (High Demand, Rival Moat > 80%)
        if demand >= 0.60 and comp_int >= 0.80:
            return "Competitive Lockout (Moat)"
        
        # 4. Distribution Failure / Dead Category
        if dist_gap < 0.40 and demand < 0.30:
            return "Weak Distribution / Dead Category"
        
        # 5. Weak Demand
        if demand < 0.35:
            return "Weak Demand"
        
        return "Established / Mature"

    df_master["Classification"] = df_master.apply(classify, axis=1)
    return df_master

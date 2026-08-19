"""
====================================================================================================
TAILWYNDZ PROPEL LATERAL DRIVE 2026 - ASSESSMENT NO. 5: "EMPTY ON THE MAP"
====================================================================================================
Production-Grade End-to-End Business Analytics & Market Expansion Engine

Target Executive: Anita Deshmukh, Commercial Director (Kestrel Beverages)

Usage:
  python analyze_empty_on_the_map.py
====================================================================================================
"""

import os
import sys
import time
import json
import pandas as pd
import numpy as np

# Add src to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.data_loader import load_all_datasets
from src.cleaning import clean_retail_panel, clean_audience_signal, clean_distribution_audit
from src.demand_model import build_independent_demand_signal
from src.wci_calculator import calculate_competitive_intensity, compute_wci_and_classify
from src.opportunity_sizing import size_market_opportunities
from src.visualization import render_all_strategic_charts

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
CHARTS_DIR = os.path.join(REPORTS_DIR, "charts")
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

def main():
    start_time = time.time()
    print("\n" + "="*95)
    print("      TAILWYNDZ PROPEL LATERAL DRIVE 2026: MARKET EXPANSION ANALYTICS ENGINE")
    print("="*95)
    print("  Problem: Empty On The Map (Energy Drink Whitespace Optimization)")
    print("  Target Horizon: 24 Months | Target Geography: 340 Districts in 12 States\n")

    # 1. Ingestion
    print("[Phase 1/6] Ingesting multi-format datasets (Excel, CSV, JSONL)...")
    data = load_all_datasets(BASE_DIR)
    df_dist_master = data["district_master"]
    df_panel_cov = data["panel_coverage"]
    df_dist_audit = data["distribution_audit"]
    df_panel = data["retail_panel"]
    df_aud = data["audience_signal"]
    print(f"  [+] Loaded {len(df_dist_master)} districts, {len(df_panel_cov):,} coverage records, {len(df_panel):,} panel rows, {len(df_aud):,} telemetry events.")

    # 2. Data Cleaning & Noise Filtering
    print("\n[Phase 2/6] Cleaning real-world anomalies, bots, and impossible outliers...")
    df_panel_clean = clean_retail_panel(df_panel)
    df_aud_clean = clean_audience_signal(df_aud)
    df_dist_summary = clean_distribution_audit(df_dist_audit)
    print(f"  [+] Ingested clean subsets: {len(df_panel_clean):,} retail transactions, {len(df_aud_clean):,} audience events.")

    # 3. Coverage Analysis
    print("\n[Phase 3/6] Quantifying 24-month panel coverage & identifying UNKNOWN markets...")
    cov_summary = df_panel_cov.groupby("District_Num_ID").agg(
        Mean_Panel_Coverage_Pct=("Panel_Coverage_Pct", "mean")
    ).reset_index()
    
    df_master = df_dist_master.merge(cov_summary, on="District_Num_ID", how="left")
    df_master["Mean_Panel_Coverage_Pct"] = df_master["Mean_Panel_Coverage_Pct"].fillna(15.0)

    # 4. Independent Demand Signal & Distribution Gap
    print("\n[Phase 4/6] Constructing independent demand signal & retail distribution gap...")
    df_master = build_independent_demand_signal(df_master, df_panel_clean, df_aud_clean)
    df_master = df_master.merge(df_dist_summary, on="District_Num_ID", how="left").fillna(0)

    # 5. Competitive Intensity & WCI Calculation
    print("\n[Phase 5/6] Calculating Competitive Intensity & Whitespace Confidence Index (WCI)...")
    comp_df = calculate_competitive_intensity(df_panel_clean)
    df_master = df_master.merge(comp_df, on="District_Num_ID", how="left").fillna(0.55)
    df_master = compute_wci_and_classify(df_master)

    # 6. Sizing Top 5 Targets & Visualizations
    print("\n[Phase 6/6] Sizing Top 5 expansion opportunities in INR and rendering strategic charts...")
    df_qualified, top5 = size_market_opportunities(df_master)
    charts = render_all_strategic_charts(df_master, top5, CHARTS_DIR)

    # Export Report Deliverables
    shortlist_path = os.path.join(REPORTS_DIR, "ranked_expansion_shortlist.csv")
    df_qualified.to_csv(shortlist_path, index=False)
    
    unknown_path = os.path.join(REPORTS_DIR, "unknown_districts_low_coverage.csv")
    df_unknown = df_master[df_master["Classification"].str.startswith("UNKNOWN")].copy()
    df_unknown.to_csv(unknown_path, index=False)
    
    full_path = os.path.join(REPORTS_DIR, "full_district_wci_classifications.csv")
    df_master.to_csv(full_path, index=False)

    # Terminal Output Presentation
    print("\n" + "="*95)
    print("                                TOP 5 EXPANSION TARGETS SHORTLIST")
    print("="*95)
    for idx, r in top5.reset_index().iterrows():
        print(f"{idx+1}. {r['District_Name_Clean']} ({r['State_Union_Territory']})")
        print(f"   • WCI Score: {r['WCI']:.4f} | Demand Signal: {r['demand_signal']:.3f} | Dist. Gap: {r['distribution_gap']*100:.1f}% | Panel Cov: {r['Mean_Panel_Coverage_Pct']:.1f}%")
        print(f"   • Demographics: Population {r['Total_Population']:,} | Retail Universe: {r['Estimated_Total_Retail_Universe']:,} outlets")
        print(f"   • Annual Value: INR {r['Annual_Opportunity_Cr']:.2f} Crores ({r['Annual_Opportunity_INR']:,.0f} INR)")
        print(f"   • Intervention Strategy: {r['Recommended_Intervention']}")
        print("-" * 95)

    print("\n--- STRATEGIC PORTFOLIO BREAKDOWN ---")
    for cat, cnt in df_master["Classification"].value_counts().items():
        print(f"  • {cat:<42}: {cnt:>3} Districts ({cnt/len(df_master)*100:.1f}%)")

    total_time = time.time() - start_time
    print(f"\n[*] Analytics Engine completed successfully in {total_time:.2f} seconds!")
    print(f"[*] Generated Reports & Charts saved in: {REPORTS_DIR}")
    print("="*95 + "\n")

if __name__ == "__main__":
    main()

"""
====================================================================================================
MODULE: data_loader.py
====================================================================================================
Handles multi-format ingestion across Excel (with offset headers), CSV, and JSON Lines.
Harmonizes messy district and outlet join keys.
====================================================================================================
"""

import os
import re
import json
import pandas as pd
import numpy as np

def resolve_data_path(base_dir, filename):
    """Finds file in data/raw or data/ directory."""
    candidates = [
        os.path.join(base_dir, "data", "raw", filename),
        os.path.join(base_dir, "data", filename),
        os.path.join(base_dir, filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise FileNotFoundError(f"Could not locate dataset file: {filename}")

def extract_numeric_id(val):
    """Robustly extract integer district ID from varied strings/numbers (e.g. 'DST_0042', 'DST-0042', 42)."""
    if pd.isna(val):
        return None
    s = str(val).strip().upper()
    s = s.replace("DST-", "").replace("DST_", "").replace("DST", "").replace("OUT-", "").replace("OUT_", "")
    try:
        return int(s)
    except:
        digits = re.findall(r"\d+", s)
        return int(digits[0]) if digits else None

DISTRICT_NAME_STANDARDIZATION = {
    "Bangalore": "Bengaluru Urban", "Bengaluru": "Bengaluru Urban", "Bangalore Urban": "Bengaluru Urban", "Bangalore (Urban)": "Bengaluru Urban",
    "Gurgaon": "Gurugram", "GURUGRAM": "Gurugram", "Gurgaon Dist.": "Gurugram",
    "Allahabad": "Prayagraj", "PRAYAGRAJ": "Prayagraj", "Allahabad (Prayagraj)": "Prayagraj",
    "Trivandrum": "Thiruvananthapuram", "TRIVANDRUM": "Thiruvananthapuram", "Thiruvananthapuram Dist": "Thiruvananthapuram",
    "Belgaum": "Belagavi", "BELAGAVI": "Belagavi", "Belgaum Dist": "Belagavi",
    "Calicut": "Kozhikode", "KOZHIKODE": "Kozhikode", "Calicut City & Rural": "Kozhikode",
    "Aurangabad": "Chhatrapati Sambhajinagar", "Aurangabad (MH)": "Chhatrapati Sambhajinagar", "Sambhajinagar": "Chhatrapati Sambhajinagar",
    "Osmanabad": "Dharashiv", "OSMANABAD": "Dharashiv", "Dharashiv (Osmanabad)": "Dharashiv",
    "Hoshangabad": "Narmadapuram", "NARMADAPURAM": "Narmadapuram", "Hoshangabad Dist": "Narmadapuram",
    "Vizag": "Visakhapatnam", "Vishakhapatnam": "Visakhapatnam", "Vizag Urban": "Visakhapatnam", "Visakhapatnam Dist": "Visakhapatnam",
    "Vijayawada Urban": "Vijayawada", "NTR District": "Vijayawada", "Bezawada": "Vijayawada",
    "YSR Kadapa": "Kadapa", "Cuddapah": "Kadapa", "Y.S.R.": "Kadapa",
    "SPSR Nellore": "Nellore", "Sri Potti Sriramulu Nellore": "Nellore",
    "East Godavari": "Rajahmundry", "Rajamahendravaram": "Rajahmundry",
    "Tirupathi": "Tirupati", "TIRUPATI": "Tirupati",
    "Kancheepuram": "Kanchipuram", "KANCHEEPURAM": "Kanchipuram",
    "Haora": "Howrah", "HOWRAH": "Howrah",
    "Hubli-Dharwad": "Dharwad", "Hubballi-Dharwad": "Dharwad", "Dharwad Dist": "Dharwad",
    "Chengalpet": "Chengalpattu", "CHENGALPATTU": "Chengalpattu", "Chengalpattu Urban": "Chengalpattu",
    "Burdwan West": "Paschim Bardhaman", "Durgapur-Asansol": "Paschim Bardhaman", "Paschim Bardhaman (Durgapur)": "Paschim Bardhaman"
}

def clean_district_name(name):
    if not isinstance(name, str):
        return name
    name_clean = name.strip()
    return DISTRICT_NAME_STANDARDIZATION.get(name_clean, name_clean)

def load_all_datasets(base_dir):
    """Loads all 5 operational datasets and master sheets."""
    excel_path = resolve_data_path(base_dir, "market_master.xlsx")
    
    # 1. District Master (Sheet 1 with Row 5 Headers)
    df_dist_master = pd.read_excel(excel_path, sheet_name="District_Master", skiprows=4)
    df_dist_master.columns = [c.strip() for c in df_dist_master.columns]
    df_dist_master["District_Num_ID"] = df_dist_master["District_Code"].apply(extract_numeric_id)
    df_dist_master["District_Name_Clean"] = df_dist_master["District_Name"].apply(clean_district_name)
    
    # 2. Panel Coverage (Sheet 2)
    df_panel_cov = pd.read_excel(excel_path, sheet_name="Panel_Coverage")
    df_panel_cov.columns = [c.strip() for c in df_panel_cov.columns]
    df_panel_cov["District_Num_ID"] = df_panel_cov["District_Ref_ID"].apply(extract_numeric_id)
    df_panel_cov["District_Name_Clean"] = df_panel_cov["District_Name"].apply(clean_district_name)
    
    # 3. Distribution Audit (Sheet 3)
    df_dist_audit = pd.read_excel(excel_path, sheet_name="Distribution_Audit")
    df_dist_audit.columns = [c.strip() for c in df_dist_audit.columns]
    df_dist_audit["District_Num_ID"] = df_dist_audit["District_ID"].apply(extract_numeric_id)
    df_dist_audit["District_Name_Clean"] = df_dist_audit["District_Name"].apply(clean_district_name)
    
    # 4. Retail Panel CSV
    panel_path = resolve_data_path(base_dir, "retail_panel.csv")
    df_panel = pd.read_csv(panel_path, low_memory=False)
    df_panel["District_Num_ID"] = df_panel["district_id"].apply(extract_numeric_id)
    
    # 5. Audience Signal JSONL
    aud_path = resolve_data_path(base_dir, "audience_signal.jsonl")
    aud_records = []
    with open(aud_path, "r", encoding="utf-8") as f:
        for line in f:
            aud_records.append(json.loads(line))
    df_aud = pd.DataFrame(aud_records)
    df_aud["District_Num_ID"] = df_aud["district_id"].apply(extract_numeric_id)
    
    # 6. Competitor Activity CSV
    comp_path = resolve_data_path(base_dir, "competitor_activity.csv")
    df_comp = pd.read_csv(comp_path, low_memory=False)
    df_comp["District_Num_ID"] = df_comp["district_id"].apply(extract_numeric_id)
    
    return {
        "district_master": df_dist_master,
        "panel_coverage": df_panel_cov,
        "distribution_audit": df_dist_audit,
        "retail_panel": df_panel,
        "audience_signal": df_aud,
        "competitor_activity": df_comp
    }

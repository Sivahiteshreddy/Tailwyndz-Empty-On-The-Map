"""
====================================================================================================
MODULE: visualization.py
====================================================================================================
Generates high-resolution strategic charts and visual decision matrices.
====================================================================================================
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

def render_all_strategic_charts(df_master, top5_targets, output_dir):
    """Renders Figure 1, Figure 2, and Figure 3."""
    os.makedirs(output_dir, exist_ok=True)
    
    # ----------------------------------------------------------------------------------
    # FIGURE 1: WCI VS DISTRIBUTION GAP MATRIX
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    palette = {
        "Likely Expansion Opportunity": "#2ca02c",
        "Competitive Lockout (Moat)": "#d62728",
        "Weak Distribution / Dead Category": "#ff7f0e",
        "UNKNOWN (Panel Blindness / Low Sampling)": "#7f7f7f",
        "Weak Demand": "#9467bd",
        "Established / Mature": "#1f77b4"
    }

    for label, grp in df_master.groupby("Classification"):
        ax.scatter(
            grp["distribution_gap"], grp["WCI"],
            label=label, color=palette.get(label, "#333333"),
            alpha=0.75, s=95 if label == "Likely Expansion Opportunity" else 35,
            edgecolors="black" if label == "Likely Expansion Opportunity" else "none",
            linewidths=1.2 if label == "Likely Expansion Opportunity" else 0
        )

    ax.axhline(y=0.70, color="#2ca02c", linestyle="--", linewidth=1.5, label="WCI Target Threshold (>= 0.70)")
    ax.axvline(x=0.40, color="#2ca02c", linestyle=":", linewidth=1.5, label="Dist. Gap Threshold (>= 0.40)")

    for idx, r in top5_targets.iterrows():
        ax.annotate(
            r["District_Name_Clean"], (r["distribution_gap"], r["WCI"]),
            textcoords="offset points", xytext=(8, 4),
            weight="bold", fontsize=8.5, color="#1b5e20"
        )

    ax.set_title("Figure 1: Whitespace Confidence Index (WCI) vs Distribution Gap", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Distribution Gap [1 - (Kestrel Stocking / Category Stocking)]", fontsize=10, fontweight="bold")
    ax.set_ylabel("Whitespace Confidence Index (WCI)", fontsize=10, fontweight="bold")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8, frameon=True)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "figure1_wci_decision_matrix.png")
    plt.savefig(chart1_path, dpi=200)
    plt.close()

    # ----------------------------------------------------------------------------------
    # FIGURE 2: PANEL COVERAGE DISTRIBUTION
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(df_master["Mean_Panel_Coverage_Pct"], bins=25, kde=True, color="#1f77b4", ax=ax)
    ax.axvline(x=60.0, color="#d62728", linestyle="--", linewidth=2.0, label="Reliability Threshold (60% Coverage)")
    ax.fill_betweenx([0, 50], 0, 60, color="#d62728", alpha=0.15, label="UNKNOWN Region (<60% Coverage)")
    ax.set_title("Figure 2: Panel Sampling Coverage Across 340 Districts", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Panel Sampling Coverage (%)", fontsize=9, fontweight="bold")
    ax.set_ylabel("District Count", fontsize=9, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "figure2_panel_coverage_distribution.png")
    plt.savefig(chart2_path, dpi=200)
    plt.close()

    # ----------------------------------------------------------------------------------
    # FIGURE 3: TOP 5 TARGET MARKET REVENUE SIZING
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bars = ax.barh(
        top5_targets["District_Name_Clean"] + " (" + top5_targets["State_Union_Territory"] + ")",
        top5_targets["Annual_Opportunity_Cr"],
        color="#2ca02c", edgecolor="#1b5e20", height=0.55
    )
    ax.bar_label(bars, fmt="INR %.2f Cr", padding=6, fontweight="bold", fontsize=9)
    ax.set_title("Figure 3: Top 5 Expansion Targets — Estimated Annual Incremental Value (INR Crores)", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Annual Revenue Opportunity (INR Crores)", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(top5_targets["Annual_Opportunity_Cr"]) * 1.30)
    ax.invert_yaxis()
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "figure3_top5_revenue_sizing.png")
    plt.savefig(chart3_path, dpi=200)
    plt.close()

    return [chart1_path, chart2_path, chart3_path]

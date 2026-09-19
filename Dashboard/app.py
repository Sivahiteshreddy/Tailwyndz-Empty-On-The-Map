
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Kestrel | Empty On The Map",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).parent
BUNDLED = BASE / "data" / "verified_highlights.csv"

# ---------- Theme ----------
st.markdown("""
<style>
    .block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1450px;}
    .hero {
        padding: 1.1rem 1.3rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 {font-size: 2.25rem; margin: 0 0 .25rem 0;}
    .hero p {margin: 0; color: #d1d5db; font-size: 1.02rem;}
    .note {
        padding: .8rem 1rem;
        border-left: 4px solid #374151;
        background: #f3f4f6;
        border-radius: 8px;
        margin: .5rem 0 1rem 0;
    }
    .decision {
        padding: 1rem;
        border-radius: 12px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
    }
    .small {color:#6b7280; font-size:.86rem;}
    .decision-card {
        padding: .9rem 1rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        min-height: 115px;
    }
    .decision-card h4 {margin:0 0 .35rem 0;}
    .decision-card p {margin:.15rem 0; color:#4b5563;}
    
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
def load_data():
    upload = st.sidebar.file_uploader(
        "Optional: upload full district WCI output",
        type=["csv", "xlsx"],
        help="Supports the project output names such as district_id, District_Name, State_Union_Territory, Demand_Signal, Mean_Distribution_Gap, Mean_Panel_Coverage, Competitiveness and WCI."
    )
    if upload is None:
        d = pd.read_csv(BUNDLED)
        source = "Verified project highlights bundled with this dashboard"
        return d, source

    if upload.name.lower().endswith(".xlsx"):
        d = pd.read_excel(upload)
    else:
        d = pd.read_csv(upload)
    source = f"Uploaded: {upload.name}"
    return d, source

df, data_source = load_data()

# Flexible column mapping for the user's eventual full output.
aliases = {
    "district_id": ["district_id","District ID","District_ID","district id"],
    "district": ["district","District","district_name","District Name","District_Name"],
    "state": ["state","State","State_Union_Territory","State/Union Territory"],
    "demand_signal": ["demand_signal","Demand Signal","Demand","Demand_Signal"],
    "distribution_gap": ["distribution_gap","Distribution Gap","Dist. Gap","Dist Gap","Mean_Distribution_Gap","Mean Distribution Gap"],
    "competitive_intensity": ["competitive_intensity","Competitive Intensity","Competition","Comp.","Competitiveness","Competitive_Intensity"],
    "wci": ["wci","WCI"],
    "panel_coverage": ["panel_coverage","Panel Coverage","Coverage","Mean Panel Coverage","Mean_Panel_Coverage","Mean_Panel_Coverage_Pct_x","Mean_Panel_Coverage_Pct_y","Mean_Panel_Coverage_Pct"],
    "action": ["action","Action","Recommended Intervention","Intervention","Recommendation","Recommended_Action"],
    "annualized_baseline_inr": ["annualized_baseline_inr","Annualized Revenue Baseline","Annualised baseline","Annualized Kestrel revenue","Annualized_Baseline_INR"],
    "status": ["status","Status","Decision","Classification","WCI_Priority","WCI_Priority_Level"],
    "group": ["group","Group"],
}


def normalize_columns(d):
    rename = {}
    lower = {str(c).strip().lower(): c for c in d.columns}
    for target, candidates in aliases.items():
        if target in d.columns:
            continue
        for c in candidates:
            key = c.strip().lower()
            if key in lower:
                rename[lower[key]] = target
                break
    d = d.rename(columns=rename).copy()
    for c in ["demand_signal","distribution_gap","competitive_intensity","wci","panel_coverage","annualized_baseline_inr"]:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    if "panel_coverage" in d.columns and d["panel_coverage"].dropna().max() > 1.5:
        d["panel_coverage"] = d["panel_coverage"] / 100
    return d

df = normalize_columns(df)

required = ["district","state","demand_signal","distribution_gap","wci","panel_coverage"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("The uploaded file is missing required columns: " + ", ".join(missing))
    st.info("This dashboard now supports the column names used in the project's wci_complete_analysis file, including State_Union_Territory, Mean_Distribution_Gap and Mean_Panel_Coverage.")
    st.stop()

# Derive decision fields when the uploaded analysis file does not contain them.
df["coverage_ok"] = df["panel_coverage"] >= 0.60
df["target_flag"] = (
    df["coverage_ok"]
    & (df["distribution_gap"] >= 0.40)
    & (df["wci"] >= 0.70)
)
df["derived_status"] = "EVALUATED"
df.loc[~df["coverage_ok"], "derived_status"] = "UNKNOWN"
df.loc[df["target_flag"], "derived_status"] = "RECOMMENDED TARGET"

if "group" not in df.columns:
    df["group"] = ""
if "action" not in df.columns:
    df["action"] = ""
if "annualized_baseline_inr" not in df.columns:
    df["annualized_baseline_inr"] = pd.NA

# ---------- Sidebar ----------
st.sidebar.title("Kestrel Decision Controls")
st.sidebar.caption(data_source)

view = st.sidebar.radio(
    "Dashboard view",
    ["Executive Overview", "India Opportunity Map", "Opportunity Shortlist", "District Explorer", "Decision Logic", "Audit & Evidence"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Project decision rules**")
st.sidebar.write("WCI ≥ 0.70")
st.sidebar.write("Distribution Gap ≥ 0.40")
st.sidebar.write("Mean Panel Coverage ≥ 60%")
st.sidebar.caption("Below 60% coverage = UNKNOWN, not zero demand.")

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>◈ Kestrel — Empty On The Map</h1>
    <p>Interactive market-expansion decision dashboard</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="note"><b>Core principle:</b> a pale sales district is not automatically an opportunity. '
    'The dashboard separates demand, distribution whitespace, competition and evidence quality.</div>',
    unsafe_allow_html=True
)

# ---------- Project-level constants ----------
TOTAL_DISTRICTS = 340
UNKNOWN = 257
RELIABLE = 83
TARGETS = 25
PALE_REJECTED = 7
TOP5_BASELINE = 52.11e6

def money_m(v):
    if pd.isna(v): return "—"
    return f"₹{v/1e6:.2f}M"

# ---------- Executive ----------
if view == "Executive Overview":
    st.subheader("Executive snapshot")

    # Decision-oriented filters: these change the view, not the methodology.
    f1, f2 = st.columns([1, 1])
    with f1:
        state_options = ["All states"] + sorted(df["state"].dropna().astype(str).unique().tolist())
        selected_state = st.selectbox("State filter", state_options, key="overview_state")
    with f2:
        lens_options = [
            "All districts",
            "Recommended targets",
            "UNKNOWN",
            "Evaluated — not a target",
        ]
        selected_lens = st.selectbox("Decision lens", lens_options, key="overview_lens")

    view_df = df.copy()
    if selected_state != "All states":
        view_df = view_df[view_df["state"].astype(str) == selected_state]

    if selected_lens == "Recommended targets":
        view_df = view_df[view_df["target_flag"]]
    elif selected_lens == "UNKNOWN":
        view_df = view_df[~view_df["coverage_ok"]]
    elif selected_lens == "Evaluated — not a target":
        view_df = view_df[view_df["coverage_ok"] & ~view_df["target_flag"]]

    st.caption(
        f"Showing {view_df['district'].nunique()} districts"
        + (f" in {selected_state}" if selected_state != "All states" else "")
        + f" under the '{selected_lens}' lens. Filters only change the display."
    )

    c1,c2,c3,c4,c5 = st.columns(5)
    district_count = int(df["district"].nunique())
    target_count = int(df["target_flag"].sum())
    unknown_count = int((~df["coverage_ok"]).sum())
    evaluated_non_target = int((df["coverage_ok"] & ~df["target_flag"]).sum())
    c1.metric("Districts", f"{district_count if district_count else TOTAL_DISTRICTS}")
    c2.metric("Recommended targets", f"{target_count if len(df) > 12 else TARGETS}")
    c3.metric("UNKNOWN", f"{unknown_count if len(df) > 12 else UNKNOWN}")
    c4.metric("Evaluated, not target", f"{evaluated_non_target if len(df) > 12 else RELIABLE - TARGETS}")
    c5.metric("Top-5 baseline", "₹52.11M")

    if len(df) > 12:
        st.success("Full 340-district WCI output connected. The dashboard is now using the uploaded district-level analysis.")
    else:
        st.info("Upload the full district WCI output to activate the complete 340-district explorer.")

    left, right = st.columns([1.05, 1.35])
    with left:
        st.markdown("### Top 5 WCI districts")
        top5 = df.sort_values("wci", ascending=False).head(5).copy()
        fig = px.bar(
            top5, x="wci", y="district", orientation="h",
            text=top5["wci"].map(lambda x: f"{x:.3f}"),
            labels={"wci":"WCI","district":""},
        )
        fig.update_layout(
            height=330, margin=dict(l=10,r=45,t=10,b=10),
            xaxis_range=[0,1], yaxis={"categoryorder":"total ascending"},
            showlegend=False
        )
        fig.update_traces(textposition="outside", hovertemplate="<b>%{y}</b><br>WCI=%{x:.3f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Opportunity ranking uses WCI. Revenue is shown separately as a commercial sizing baseline.")

    with right:
        st.markdown("### Opportunity matrix")
        plot_df = view_df.copy()
        plot_df["decision"] = plot_df["derived_status"]

        # Keep the matrix readable: labels only for recommended targets.
        plot_df["label"] = plot_df["district"].where(plot_df["target_flag"], "")
        plot_df["decision"] = pd.Categorical(
            plot_df["decision"],
            categories=["UNKNOWN","EVALUATED","RECOMMENDED TARGET"],
            ordered=True
        )

        fig = px.scatter(
            plot_df,
            x="distribution_gap",
            y="demand_signal",
            size="wci",
            color="decision",
            text="label",
            hover_name="district",
            hover_data={
                "state": True,
                "wci": ":.3f",
                "panel_coverage": ":.1%",
                "distribution_gap": ":.3f",
                "demand_signal": ":.3f",
                "decision": True,
                "label": False,
            },
            category_orders={"decision":["UNKNOWN","EVALUATED","RECOMMENDED TARGET"]},
            labels={
                "distribution_gap":"Distribution Gap",
                "demand_signal":"Demand Signal",
                "decision":"Decision status",
            },
        )
        fig.add_vline(x=0.40, line_dash="dash", annotation_text="Gap ≥ 0.40", annotation_position="top")
        fig.add_hline(y=0.70, line_dash="dash", annotation_text="Demand reference 0.70", annotation_position="top left")
        fig.update_traces(textposition="top center", marker=dict(opacity=0.72, line=dict(width=0.5)))
        fig.update_layout(
            height=430,
            margin=dict(l=10,r=10,t=25,b=10),
            xaxis=dict(range=[0,1], gridcolor="#e5e7eb"),
            yaxis=dict(range=[0,1], gridcolor="#e5e7eb"),
            legend_title_text="",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("District names are shown only for recommended targets; hover over any point for full metrics.")

    st.markdown("### Decision portfolio")
    st.info("Use the shortlist to identify priority districts, then use District Explorer to review the supporting evidence.")
    a,b,c = st.columns(3)
    with a:
        st.markdown('<div class="decision-card"><h4>🎯 Recommended targets</h4><p><b>25 districts</b></p><p>Reliable evidence + distribution gap ≥ 0.40 + WCI ≥ 0.70.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="decision-card"><h4>❓ UNKNOWN</h4><p><b>257 districts</b></p><p>Coverage below 60%; do not interpret this as zero demand.</p></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="decision-card"><h4>◌ Evaluated, not target</h4><p><b>58 districts</b></p><p>Coverage is sufficient, but the full target rule is not met.</p></div>', unsafe_allow_html=True)

    st.markdown("### The three stories the dashboard should make obvious")
    a,b,c = st.columns(3)
    with a:
        st.markdown("**1. TARGET**")
        st.write("Strong independent demand + large distribution whitespace + reliable evidence.")
        st.caption("Example: Dharwad")
    with b:
        st.markdown("**2. UNKNOWN**")
        st.write("Low panel coverage means the evidence is insufficient to conclude demand is weak.")
        st.caption("257 of 340 districts")
    with c:
        st.markdown("**3. EVALUATED, NOT TARGET**")
        st.write("Reliable evidence exists, but the district does not clear the whitespace decision rule.")
        st.caption("58 districts in the full analysis")




# ---------- India opportunity map ----------
elif view == "India Opportunity Map":
    st.subheader("India Opportunity Map")
    st.caption(
        "State-level visual navigation of the 340-district assessment. "
        "District-level decisions remain in the underlying analysis and District Explorer."
    )

    state_centroids = {
        "Andhra Pradesh": (15.91, 79.74),
        "Arunachal Pradesh": (28.22, 94.73),
        "Assam": (26.20, 92.94),
        "Bihar": (25.10, 85.31),
        "Chhattisgarh": (21.28, 81.87),
        "Goa": (15.30, 74.12),
        "Gujarat": (22.26, 71.19),
        "Haryana": (29.06, 76.09),
        "Himachal Pradesh": (31.10, 77.17),
        "Jharkhand": (23.61, 85.28),
        "Karnataka": (15.32, 75.71),
        "Kerala": (10.85, 76.27),
        "Madhya Pradesh": (23.47, 77.95),
        "Maharashtra": (19.75, 75.71),
        "Manipur": (24.66, 93.91),
        "Meghalaya": (25.47, 91.37),
        "Mizoram": (23.16, 92.94),
        "Nagaland": (26.16, 94.56),
        "Odisha": (20.95, 85.10),
        "Punjab": (31.15, 75.34),
        "Rajasthan": (27.02, 74.22),
        "Sikkim": (27.53, 88.51),
        "Tamil Nadu": (11.13, 78.66),
        "Telangana": (17.99, 79.55),
        "Tripura": (23.94, 91.99),
        "Uttar Pradesh": (26.85, 80.95),
        "Uttarakhand": (30.07, 79.02),
        "West Bengal": (23.68, 87.75),
        "Andaman and Nicobar Islands": (11.74, 92.66),
        "Chandigarh": (30.73, 76.78),
        "Delhi": (28.61, 77.21),
        "Jammu and Kashmir": (33.78, 76.58),
        "Ladakh": (34.15, 77.58),
        "Puducherry": (11.91, 79.81),
    }

    # Build state-level map summaries from explicit decision flags.
    # Keep this aggregation simple and robust across pandas versions.
    map_source = df.copy()
    map_source["unknown_flag"] = ~map_source["coverage_ok"].astype(bool)
    map_source["evaluated_not_target_flag"] = (
        map_source["coverage_ok"].astype(bool)
        & ~map_source["target_flag"].astype(bool)
    )

    map_df = (
        map_source.groupby("state", dropna=False)
        .agg(
            districts=("district", "nunique"),
            recommended=("target_flag", "sum"),
            unknown=("unknown_flag", "sum"),
            evaluated_not_target=("evaluated_not_target_flag", "sum"),
            max_wci=("wci", "max"),
        )
        .reset_index()
    )

    target_names = (
        df[df["target_flag"]]
        .groupby("state")["district"]
        .apply(lambda s: ", ".join(s.dropna().astype(str).tolist()))
        .to_dict()
    )
    map_df["target_districts"] = map_df["state"].map(target_names).fillna("None")

    map_df["lat"] = map_df["state"].map(lambda x: state_centroids.get(str(x), (None, None))[0])
    map_df["lon"] = map_df["state"].map(lambda x: state_centroids.get(str(x), (None, None))[1])
    map_df = map_df.dropna(subset=["lat", "lon"]).copy()

    m1, m2, m3 = st.columns(3)
    m1.metric("Recommended districts", int(df["target_flag"].sum()))
    m2.metric("UNKNOWN districts", int((~df["coverage_ok"]).sum()))
    m3.metric("Evaluated — not target", int((df["coverage_ok"] & ~df["target_flag"]).sum()))

    fig = px.scatter_geo(
        map_df,
        lat="lat",
        lon="lon",
        size="recommended",
        color="recommended",
        hover_name="state",
        hover_data={
            "districts": True,
            "recommended": True,
            "unknown": True,
            "evaluated_not_target": True,
            "max_wci": ":.3f",
            "target_districts": True,
            "lat": False,
            "lon": False,
        },
        labels={
            "districts": "Assessment districts",
            "recommended": "Recommended",
            "unknown": "UNKNOWN",
            "evaluated_not_target": "Evaluated — not target",
            "max_wci": "Highest WCI",
            "target_districts": "Recommended district(s)",
        },
        color_continuous_scale="Blues",
        size_max=28,
    )
    fig.update_geos(
        scope="asia",
        projection_type="natural earth",
        center={"lat": 22.5, "lon": 79},
        lataxis_range=[6, 38],
        lonaxis_range=[67, 98],
        showland=True,
        showcountries=True,
        countrycolor="#9ca3af",
        showcoastlines=True,
        coastlinecolor="#9ca3af",
        showocean=True,
        oceancolor="#f8fafc",
        landcolor="#ffffff",
    )
    fig.update_layout(
        height=620,
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_colorbar_title="Recommended<br>districts",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### How to read the map")
    st.write(
        "Each bubble represents a state-level location anchor, not a district boundary. "
        "Bubble size shows the number of recommended assessment districts in that state. "
        "Hover to see the number of recommended, UNKNOWN and evaluated-not-target districts, "
        "plus the recommended district names."
    )
    st.info(
        "The assessment contains 340 districts, while publicly available district-boundary datasets "
        "use different administrative vintages. This map therefore avoids drawing potentially mismatched "
        "district polygons; the decision itself remains district-level."
    )

    st.markdown("### Priority states by recommended districts")
    state_table = map_df.sort_values(
        ["recommended", "max_wci"], ascending=[False, False]
    )[[
        "state", "districts", "recommended", "unknown",
        "evaluated_not_target", "max_wci", "target_districts"
    ]].copy()
    state_table.columns = [
        "State", "Assessment districts", "Recommended",
        "UNKNOWN", "Evaluated — not target", "Highest WCI", "Recommended district(s)"
    ]
    st.dataframe(
        state_table.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Highest WCI": st.column_config.NumberColumn(format="%.3f"),
        },
    )


# ---------- Opportunity shortlist ----------
elif view == "Opportunity Shortlist":
    st.subheader("Opportunity Shortlist")
    st.caption("A decision-ready view: shortlist the districts first, then explain the evidence behind each one.")

    targets = df[df["target_flag"]].copy().sort_values(
        ["wci", "distribution_gap", "demand_signal"], ascending=False
    )

    # If the full output is loaded, keep the shortlist driven by the project's actual gates.
    st.markdown("### Recommended targets")
    st.write(
        "These districts clear all three project gates: panel coverage ≥ 60%, "
        "distribution gap ≥ 0.40, and WCI ≥ 0.70."
    )

    display_cols = ["district", "state", "wci", "demand_signal", "distribution_gap", "panel_coverage"]
    if "annualized_baseline_inr" in targets.columns and targets["annualized_baseline_inr"].notna().any():
        display_cols.append("annualized_baseline_inr")

    shortlist = targets[display_cols].copy()
    shortlist.columns = [
        "District", "State", "WCI", "Demand", "Distribution Gap", "Panel Coverage"
    ] + (["Annualized Baseline"] if len(display_cols) == 7 else [])

    if "Annualized Baseline" in shortlist.columns:
        shortlist["Annualized Baseline"] = shortlist["Annualized Baseline"].apply(money_m)

    st.dataframe(
        shortlist.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "WCI": st.column_config.NumberColumn(format="%.3f"),
            "Demand": st.column_config.NumberColumn(format="%.3f"),
            "Distribution Gap": st.column_config.NumberColumn(format="%.3f"),
            "Panel Coverage": st.column_config.NumberColumn(format="%.1%"),
        },
    )

    st.markdown("### Why this district?")
    if len(targets) == 0:
        st.info("No recommended targets are present in the loaded dataset.")
    else:
        labels = [
            f"{r.district} — {r.state}"
            for _, r in targets.iterrows()
        ]
        chosen = st.selectbox("Choose a recommended district", labels, key="shortlist_district")
        selected = targets.iloc[labels.index(chosen)]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("WCI", f"{selected.wci:.3f}")
        c2.metric("Demand", f"{selected.demand_signal:.3f}")
        c3.metric("Distribution Gap", f"{selected.distribution_gap:.3f}")
        c4.metric("Panel Coverage", f"{selected.panel_coverage:.1%}")

        st.success(
            f"{selected.district} clears the recommendation rule. "
            "The business case is distribution expansion supported by targeted marketing."
        )

        left, right = st.columns([1.05, 1])

        with left:
            st.markdown("#### Evidence gates")
            gate_df = pd.DataFrame({
                "Gate": ["Panel coverage", "Distribution gap", "WCI"],
                "Observed": [
                    f"{selected.panel_coverage:.1%}",
                    f"{selected.distribution_gap:.3f}",
                    f"{selected.wci:.3f}",
                ],
                "Threshold": ["≥ 60%", "≥ 0.40", "≥ 0.70"],
                "Result": ["PASS", "PASS", "PASS"],
            })
            st.dataframe(gate_df, use_container_width=True, hide_index=True)

        with right:
            st.markdown("#### Commercial sizing")
            if "annualized_baseline_inr" in selected.index and pd.notna(selected["annualized_baseline_inr"]):
                st.metric("Annualized baseline", money_m(selected["annualized_baseline_inr"]))
                st.caption("Historical Kestrel revenue annualized for sizing; not guaranteed incremental revenue.")
            else:
                st.info("Revenue baseline is not present in the loaded file.")

        st.markdown("#### Decision rationale")
        st.write(
            f"“I would not call {selected.district} an opportunity just because its observed sales are low. "
            f"The independent demand signal is {selected.demand_signal:.3f}, the distribution gap is "
            f"{selected.distribution_gap:.3f}, and panel coverage is {selected.panel_coverage:.1%}. "
            f"Because the district clears the evidence, distribution and WCI gates, I would prioritize "
            "distribution expansion and targeted marketing.”"
        )

    st.markdown("---")
    st.markdown("### What about the other 315 districts?")
    st.write(
        "The shortlist is intentionally not a simple sales ranking. The remaining districts fall into "
        "two decision states: UNKNOWN where panel coverage is below 60%, and EVALUATED — NOT A TARGET "
        "where evidence is sufficient but the recommendation rule is not met."
    )
    u, e = st.columns(2)
    u.metric("UNKNOWN", int((~df["coverage_ok"]).sum()))
    e.metric("Evaluated — not target", int((df["coverage_ok"] & ~df["target_flag"]).sum()))


# ---------- District explorer ----------
elif view == "District Explorer":
    st.subheader("District Explorer")
    st.caption("Use this view to explain *why* a district is or is not a whitespace case.")

    options = (df["district"] + " — " + df["state"]).sort_values().tolist()
    selected = st.selectbox("Select a district", options)
    row = df.loc[(df["district"] + " — " + df["state"]) == selected].iloc[0]

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Demand Signal", f"{row.demand_signal:.3f}")
    c2.metric("Distribution Gap", f"{row.distribution_gap:.3f}")
    c3.metric("Competitive Intensity", "—" if pd.isna(row.competitive_intensity) else f"{row.competitive_intensity:.3f}")
    c4.metric("WCI", f"{row.wci:.3f}")
    c5.metric("Coverage", f"{row.panel_coverage:.1%}")

    st.markdown("### Decision path")
    coverage_ok = row.panel_coverage >= .60
    gap_ok = row.distribution_gap >= .40
    wci_ok = row.wci >= .70

    stages = [
        ("Evidence gate", coverage_ok, f"Coverage {row.panel_coverage:.1%} ≥ 60%"),
        ("Distribution gate", gap_ok, f"Gap {row.distribution_gap:.3f} ≥ 0.40"),
        ("WCI gate", wci_ok, f"WCI {row.wci:.3f} ≥ 0.70"),
    ]
    cols2 = st.columns(3)
    for col, (name, ok, detail) in zip(cols2, stages):
        with col:
            icon = "✓" if ok else "✕"
            st.markdown(f"### {icon} {name}")
            st.write(detail)

    st.markdown("---")
    left,right = st.columns([1,1])
    with left:
        st.markdown("### WCI contribution view")
        if not pd.isna(row.competitive_intensity):
            vals = {
                "Demand contribution": .45 * row.demand_signal,
                "Distribution contribution": .35 * row.distribution_gap,
                "Competition contribution": .20 * (1 - row.competitive_intensity),
            }
            fig = go.Figure(go.Bar(
                x=list(vals.values()), y=list(vals.keys()), orientation="h",
                text=[f"{v:.3f}" for v in vals.values()], textposition="outside"
            ))
            fig.update_layout(height=280, xaxis_title="Contribution to WCI", margin=dict(l=10,r=50,t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Competitive intensity is not present in the bundled rejected-district summary. The final WCI is retained exactly as reported by the completed analysis.")

    with right:
        st.markdown("### Commercial interpretation")
        if bool(row["target_flag"]):
            st.success("RECOMMENDED TARGET — distribution expansion plus targeted marketing.")
            st.write("The district clears the project's evidence, distribution-gap and WCI gates.")
            if pd.notna(row.get("annualized_baseline_inr")):
                st.metric("Annualized baseline", money_m(row.annualized_baseline_inr))
                st.caption("Sizing baseline from historical Kestrel revenue; not guaranteed incremental revenue.")
        elif not bool(row["coverage_ok"]):
            st.warning("UNKNOWN — insufficient panel evidence.")
            st.write("Coverage is below 60%, so the project does not treat this district as weak demand or as an expansion rejection.")
        else:
            st.info("EVALUATED — does not clear the full target rule.")
            if row.demand_signal < .10:
                st.write("Reason: weak independent demand.")
            elif row.distribution_gap < .40:
                st.write("Reason: distribution gap is below 0.40.")
            elif row.wci < .70:
                st.write("Reason: WCI is below 0.70.")
            else:
                st.write("Reason: the district does not meet the complete recommendation rule.")

# ---------- Decision logic ----------
elif view == "Decision Logic":
    st.subheader("How the decision is made")
    st.write("The dashboard intentionally mirrors the assessment logic rather than inventing a new score.")

    st.latex(r"WCI = 0.45 \times Demand\ Signal + 0.35 \times Distribution\ Gap + 0.20 \times (1 - Competitive\ Intensity)")

    a,b,c = st.columns(3)
    a.metric("WCI threshold", "≥ 0.70")
    b.metric("Distribution gap", "≥ 0.40")
    c.metric("Panel coverage", "≥ 60%")

    st.markdown("### Evidence-first decision tree")
    st.code("""
Panel Coverage < 60%
        ↓
     UNKNOWN
        ↓
Do not infer zero demand

Panel Coverage ≥ 60%
        ↓
Evaluate Demand + Distribution + Competition
        ↓
WCI ≥ 0.70 AND Distribution Gap ≥ 0.40
        ↓
Recommended target
""", language="text")

    st.markdown("### Why this is different from ranking pale sales")
    st.write(
        "A low-sales district can be low because demand is weak, because Kestrel is poorly distributed, "
        "or because the panel does not observe enough of the market. The WCI framework separates those explanations."
    )

    st.markdown("### Market-size normalization")
    st.write(
        "The analysis avoids ranking districts simply by absolute category volume. The dashboard therefore emphasizes normalized signals and WCI, while revenue is shown separately as a commercial sizing baseline."
    )

# ---------- Audit ----------
else:
    st.subheader("Audit & Evidence")
    st.caption("Review the data-quality controls and evidence checks used to support the decision.")

    audit = [
        ("Retail Panel exact duplicates", "27,746"),
        ("Audience exact duplicates", "7,645"),
        ("Kestrel Sales duplicates", "979"),
        ("Competitor Activity duplicates", "816"),
        ("Negative unit prices", "2,115"),
        ("Invalid audience ages", "1,423"),
        ("Impossible distribution rows", "159"),
        ("Districts aligned", "340 / 340"),
        ("District-month framework", "8,160"),
        ("Below 60% coverage", "6,314 / 8,160"),
    ]
    adf = pd.DataFrame(audit, columns=["Audit check","Finding"])
    st.dataframe(adf, use_container_width=True, hide_index=True)

    st.markdown("### Coverage is the most important caveat")
    x,y,z = st.columns(3)
    x.metric("District-month observations", "8,160")
    y.metric("Below 60% coverage", "77.4%")
    z.metric("Districts UNKNOWN", "257 / 340")

    st.warning(
        "UNKNOWN is an evidence classification, not a negative business verdict. "
        "The completed analysis explicitly avoids treating low observed panel sales as zero demand."
    )

    st.markdown("### What the dashboard does not claim")
    st.write("- ₹52.11M is a commercial sizing baseline, not guaranteed incremental revenue.")
    st.write("- WCI is a prioritization tool, not a revenue forecast.")
    st.write("- Hidden ground-truth district-type labels are not used for final decisions.")
    st.write("- The bundled dashboard dataset is a verified highlights layer; the uploaded file provides the full 340-district output used in this session.")

st.markdown("---")
st.caption("Kestrel Beverages | Empty On The Map | Interactive companion to the memo and presentation")

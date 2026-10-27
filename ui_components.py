"""
UI Components and Visualizations for Reliance Retail Business Simulator
PROMPT 14 — What-If Business Simulator: Can Sales Grow 20%?
SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA. FOR ILLUSTRATIVE MODELING ONLY.

This module provides:
- Custom CSS injection (Dark navy/charcoal styling with restrained purple accents and modern typography)
- Synthetic data disclaimer banners
- Custom responsive KPI metric cards
- Plotly interactive gauges for the 5 capacity pillars
- Bottleneck heatmaps, waterfall P&L charts, radar charts, and sensitivity matrices
- Connected numbered flowchart for the computational algorithm
- Downloadable Executive HTML & CSV reports
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import base64
from datetime import datetime

# Primary Theme Color Tokens
NAVY_BG = "#0b0f19"
SURFACE_CARD = "#1e293b"
SURFACE_BORDER = "#334155"
ACCENT_PURPLE = "#8b5cf6"
ACCENT_LIGHT_PURPLE = "#c4b5fd"
TEXT_PRIMARY = "#f8fafc"
TEXT_MUTED = "#94a3b8"
COLOR_SUCCESS = "#10b981"
COLOR_WARNING = "#f59e0b"
COLOR_DANGER = "#ef4444"
COLOR_CYAN = "#06b6d4"

def inject_custom_styles():
    """
    Injects professional dark navy/charcoal styling with restrained purple accents
    and clean system / Inter typography.
    """
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    .stApp {{
        background-color: {NAVY_BG};
        color: {TEXT_PRIMARY};
    }}

    /* Global Header Bar */
    .top-banner {{
        background: linear-gradient(90deg, #1e1b4b 0%, #31104b 50%, #1e1b4b 100%);
        border: 1px solid #6366f1;
        border-radius: 8px;
        padding: 10px 18px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .top-banner-text {{
        color: #e0e7ff;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    .synthetic-badge {{
        background-color: #4f46e5;
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        border: 1px solid #818cf8;
    }}

    /* Metric Cards */
    .metric-card {{
        background: {SURFACE_CARD};
        border: 1px solid {SURFACE_BORDER};
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }}
    .metric-card:hover {{
        border-color: {ACCENT_PURPLE};
        transform: translateY(-2px);
    }}
    .metric-title {{
        color: {TEXT_MUTED};
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
    }}
    .metric-value {{
        color: {TEXT_PRIMARY};
        font-size: 1.65rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 6px;
    }}
    .metric-delta {{
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }}
    .delta-positive {{ color: {COLOR_SUCCESS}; }}
    .delta-negative {{ color: {COLOR_DANGER}; }}
    .delta-neutral {{ color: {TEXT_MUTED}; }}

    /* Status Pill */
    .status-pill {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
    }}

    /* Sidebar overrides */
    [data-testid="stSidebar"] {{
        background-color: #0f172a !important;
        border-right: 1px solid {SURFACE_BORDER};
    }}
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: {ACCENT_LIGHT_PURPLE} !important;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: #0f172a;
        padding: 6px;
        border-radius: 8px;
        border: 1px solid {SURFACE_BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 42px;
        white-space: pre-wrap;
        border-radius: 6px;
        color: {TEXT_MUTED};
        font-weight: 500;
        font-size: 0.88rem;
        padding: 6px 14px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #312e81 !important;
        color: #ffffff !important;
        border: 1px solid {ACCENT_PURPLE} !important;
        font-weight: 600 !important;
    }}

    /* Card Panels */
    .content-box {{
        background: {SURFACE_CARD};
        border: 1px solid {SURFACE_BORDER};
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 20px;
    }}

    /* Flowchart steps */
    .flow-step {{
        background: #1e1b4b;
        border: 1px solid #4338ca;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        display: flex;
        gap: 14px;
        align-items: flex-start;
    }}
    .step-number {{
        background: {ACCENT_PURPLE};
        color: #ffffff;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.95rem;
        flex-shrink: 0;
    }}
    .step-content-title {{
        color: #e0e7ff;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 4px;
    }}
    .step-content-desc {{
        color: {TEXT_MUTED};
        font-size: 0.84rem;
        line-height: 1.45;
    }}

    /* Buttons */
    .stButton>button {{
        background-color: #4338ca;
        color: #ffffff;
        border: 1px solid {ACCENT_PURPLE};
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }}
    .stButton>button:hover {{
        background-color: #4f46e5;
        border-color: #a78bfa;
        color: #ffffff;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_top_banner():
    """
    Renders top persistent disclaimer banner.
    """
    html = """
    <div class="top-banner">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:1.2rem;">🔬</span>
            <span class="top-banner-text">
                RELIANCE RETAIL WHAT-IF BUSINESS SIMULATOR &bull; CAN SALES GROW 20%?
            </span>
        </div>
        <div class="synthetic-badge">
            SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_kpi_card(title: str, value: str, delta: str = None, delta_type: str = "neutral", subtitle: str = None):
    """
    Renders styled executive KPI card.
    """
    delta_class = f"delta-{delta_type}"
    delta_arrow = "▲ " if delta_type == "positive" else ("▼ " if delta_type == "negative" else "• ")
    delta_html = f'<div class="metric-delta {delta_class}">{delta_arrow}{delta}</div>' if delta else ""
    subtitle_html = f'<div style="font-size:0.75rem; color:{TEXT_MUTED}; margin-top:4px;">{subtitle}</div>' if subtitle else ""

    html = f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_pillar_gauge(pillar_name: str, utilization_pct: float, target_cap: str = "100%"):
    """
    Builds a Plotly mini-gauge for each operational pillar with green, amber, red zones.
    """
    # Color logic
    if utilization_pct <= 85.0:
        bar_color = COLOR_SUCCESS
    elif utilization_pct <= 100.0:
        bar_color = COLOR_WARNING
    else:
        bar_color = COLOR_DANGER

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=utilization_pct,
        number={"suffix": "%", "font": {"size": 20, "color": TEXT_PRIMARY, "family": "Inter"}},
        title={"text": f"<b>{pillar_name}</b><br><span style='font-size:0.72rem;color:{TEXT_MUTED}'>Max Limit: {target_cap}</span>", "font": {"size": 13, "color": TEXT_MUTED, "family": "Inter"}},
        gauge={
            "axis": {"range": [0, 140], "tickwidth": 1, "tickcolor": "#475569", "tickfont": {"size": 9, "color": TEXT_MUTED}},
            "bar": {"color": bar_color, "thickness": 0.3},
            "bgcolor": "#1e293b",
            "borderwidth": 1,
            "bordercolor": "#334155",
            "steps": [
                {"range": [0, 85], "color": "rgba(16, 185, 129, 0.15)"},
                {"range": [85, 100], "color": "rgba(245, 158, 11, 0.20)"},
                {"range": [100, 140], "color": "rgba(239, 68, 68, 0.25)"}
            ],
            "threshold": {
                "line": {"color": "#ef4444", "width": 3},
                "thickness": 0.8,
                "value": 100.0
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=190,
        margin=dict(l=15, r=15, t=35, b=10)
    )
    return fig

def render_waterfall_pnl(res: dict):
    """
    Generates Plotly Waterfall Chart showing baseline EBITDA to realized scenario EBITDA.
    """
    baseline_ebitda = res["baseline_ebitda_cr"]
    incremental_rev = res["incremental_revenue_cr"]
    incremental_cogs = -(res["realized_gross_profit_cr"] - baseline_ebitda) # proportional
    
    cb = res["cost_breakdown"]
    ot_cost = -cb["Overtime Premium"]
    temp_cost = -cb["Temp Hiring & Training"]
    wh_surcharge = -cb["Warehouse 2nd Shift Surcharge"]
    tpl_surcharge = -cb["Logistics 3PL Flex Surcharge"]
    sup_expedite = -(cb["Supplier Expedite & Dual-Source"] + cb["Supplier Reservation Retainers"])
    carrying_finance = -(cb["Inventory Holding Cost"] + cb["Working Capital Financing"])
    lost_sales_hit = -res["lost_sales_cr"]
    realized_ebitda = res["ebitda_cr"]

    # Build waterfall items
    labels = [
        "Baseline EBITDA",
        "Target Rev Lift",
        "Lost Sales (Stockouts)",
        "Overtime & Temp Staff",
        "Warehouse 2nd Shift",
        "Logistics 3PL Surcharges",
        "Supplier Dual-Source/Expedite",
        "Inventory Carrying & Interest",
        "Realized EBITDA"
    ]
    measures = ["absolute", "relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"]
    y_values = [
        baseline_ebitda,
        res["unconstrained_target_rev_cr"] - res["baseline_total_rev_cr"],
        lost_sales_hit,
        ot_cost + temp_cost,
        wh_surcharge,
        tpl_surcharge,
        sup_expedite,
        carrying_finance,
        realized_ebitda
    ]

    fig = go.Figure(go.Waterfall(
        name="P&L Bridge",
        orientation="v",
        measure=measures,
        x=labels,
        textposition="outside",
        text=[f"₹{abs(v):,.0f} Cr" for v in y_values],
        y=y_values,
        connector={"line": {"color": "#64748b"}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": "#8b5cf6"}}
    ))

    fig.update_layout(
        title={"text": "<b>EBITDA Bridge: From Baseline to Realized Scenario (₹ Crores)</b>", "font": {"size": 15, "color": TEXT_PRIMARY, "family": "Inter"}},
        paper_bgcolor=SURFACE_CARD,
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_MUTED, "family": "Inter"},
        yaxis={"title": "₹ Crores", "gridcolor": "#334155"},
        xaxis={"tickangle": -30},
        height=420,
        margin=dict(l=30, r=20, t=50, b=80)
    )
    return fig

def render_bottleneck_heatmap(products_df: pd.DataFrame, regions_df: pd.DataFrame, growth_target_pct: float):
    """
    Renders an illustrative Category x Region capacity stress heatmap.
    """
    cats = products_df["category_name"].tolist()
    regs = [r.split(" ")[0] for r in regions_df["region_name"].tolist()]
    
    # Calculate stress matrix
    matrix = []
    for cat in products_df.itertuples():
        row = []
        for reg in regions_df.itertuples():
            # Base stress depends on category lead time & regional store density
            base_stress = 80.0 + (growth_target_pct * 1.05)
            if "Electronics" in cat.category_name or "Fashion" in cat.category_name:
                base_stress += 8.0
            if "West" in reg.region_name or "North" in reg.region_name:
                base_stress += 4.5
            row.append(round(min(145.0, base_stress), 1))
        matrix.append(row)

    fig = px.imshow(
        matrix,
        x=regs,
        y=cats,
        color_continuous_scale=[[0, "#10b981"], [0.55, "#f59e0b"], [1, "#ef4444"]],
        labels=dict(x="Geographic Zone", y="Product Pillar", color="Capacity Stress %"),
        text_auto=True
    )
    fig.update_layout(
        title={"text": "<b>Operational Bottleneck Stress Matrix (% Capacity Utilized)</b>", "font": {"size": 14, "color": TEXT_PRIMARY, "family": "Inter"}},
        paper_bgcolor=SURFACE_CARD,
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_MUTED, "family": "Inter"},
        height=340,
        margin=dict(l=20, r=20, t=45, b=25)
    )
    return fig

def render_radar_comparison(scenarios_df: pd.DataFrame):
    """
    Radar chart comparing Scenario Feasibility, OTIF, Margin, and Speed.
    """
    categories = ["Feasibility", "OTIF Service", "Margin %", "Speed / Low Lead Time", "Low Capital Tied"]

    fig = go.Figure()

    # Compare 3 key scenarios: Baseline, Unmitigated, Balanced
    sc_subset = scenarios_df.loc[scenarios_df["Scenario"].str.contains("Baseline|Unmitigated|Balanced", case=False)]
    
    colors = ["#94a3b8", "#ef4444", "#10b981"]
    for idx, (_, row) in enumerate(sc_subset.iterrows()):
        feas = float(row["Feasibility Score"])
        otif = float(row["OTIF Service %"].replace("%", ""))
        margin = float(row["EBITDA Margin %"].replace("%", "")) * 4.5  # scaled to 100
        speed = 100.0 - (float(row["Lead Time"].replace(" wks", "")) * 12.0)
        cap_tied = 100.0 - min(80.0, float(row["Working Capital Locked (₹ Cr)"]) / 35.0)

        r_values = [feas, otif, min(100.0, margin), max(20.0, speed), max(20.0, cap_tied)]
        r_values.append(r_values[0])  # close loop

        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=categories + [categories[0]],
            fill="toself",
            name=row["Scenario"].split(". ")[1],
            line=dict(color=colors[idx % len(colors)], width=2)
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#64748b"),
            bgcolor="#1e293b"
        ),
        paper_bgcolor=SURFACE_CARD,
        font=dict(color=TEXT_MUTED, family="Inter"),
        title=dict(text="<b>Multi-Dimensional Scenario Trade-Off Radar</b>", font=dict(size=14, color=TEXT_PRIMARY, family="Inter")),
        height=380,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def render_monte_carlo_distribution(mc_res: dict):
    """
    Renders histogram and density for Monte Carlo EBITDA with P10, P50, P90 markers.
    """
    samples = mc_res["ebitda_samples"]
    p10 = mc_res["ebitda_p10"]
    p50 = mc_res["ebitda_p50"]
    p90 = mc_res["ebitda_p90"]

    fig = px.histogram(
        x=samples,
        nbins=45,
        labels={"x": "Realized Scenario EBITDA (₹ Crores)"},
        color_discrete_sequence=["#8b5cf6"],
        opacity=0.75
    )
    # Add vertical lines for percentiles
    fig.add_vline(x=p10, line_dash="dash", line_color="#ef4444", annotation_text=f"P10: ₹{p10:,.0f} Cr", annotation_position="top left", annotation_font_color="#ef4444")
    fig.add_vline(x=p50, line_dash="solid", line_color="#38bdf8", annotation_text=f"P50 (Median): ₹{p50:,.0f} Cr", annotation_position="top right", annotation_font_color="#38bdf8")
    fig.add_vline(x=p90, line_dash="dash", line_color="#10b981", annotation_text=f"P90: ₹{p90:,.0f} Cr", annotation_position="top right", annotation_font_color="#10b981")

    fig.update_layout(
        title={"text": f"<b>Monte Carlo Stress Simulation (1,000 Iterations) — Stochastic Demand, Delays & Wages</b>", "font": {"size": 14, "color": TEXT_PRIMARY, "family": "Inter"}},
        paper_bgcolor=SURFACE_CARD,
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_MUTED, "family": "Inter"},
        yaxis={"title": "Frequency Count", "gridcolor": "#334155"},
        xaxis={"gridcolor": "#334155"},
        height=380,
        margin=dict(l=30, r=20, t=50, b=40)
    )
    return fig

def render_algorithm_flowchart():
    """
    Connected numbered visual flowchart explaining the computation pipeline.
    """
    steps = [
        ("1", "Demand & Revenue Translation", "User specifies Growth Target (e.g. +20%) and Planning Horizon (1-12 months). The algorithm scales baseline units across 5 product segments and 4 geographic zones, computing unconstrained target revenue and base COGS."),
        ("2", "Workforce & Staffing Capacity Check", "Computes total required labor hours across store customer associates, DC fulfillment pickers, and delivery operators. Compares demand against regular hours, overtime legal limits (max 20%), temporary seasonal hiring, and cross-skilling efficiency gains."),
        ("3", "Supplier Network & Lead Time Bottleneck", "Evaluates tier-1 supplier maximum burst production thresholds (+11% to +18%). Triggers dual-sourcing secondary suppliers and expedited freight surcharges. Unmitigated supply deficits induce stockout penalties."),
        ("4", "Warehouse Throughput & Cross-Docking", "Assesses daily handling throughput across 8 mega-distribution centers. Models second/night shift activation (+40% capacity) and modular cross-docking (+12% speed) against warehouse handling unit costs."),
        ("5", "Logistics Fleet & Last-Mile Flex", "Calculates required daily dispatches vs dedicated fleet capacity. Dispatches spillover delivery volume to elastic contracted 3PL partners at contracted surge rates to protect delivery SLA."),
        ("6", "Working Capital & Cash Flow Modeling", "Computes required inventory buffer (safety stock days of cover), incremental capital tied up, inventory carrying costs (18% p.a.), and accounts receivable (DSO 7d) vs payable credit terms (DPO 42d)."),
        ("7", "OTIF Service Level & Realized P&L Bridge", "Synthesizes customer service level (OTIF %). Applies non-linear lost sales penalties for unfulfilled demand. Outputs Realized Revenue, Net Gross Profit, Total OpEx, EBITDA, and Feasibility Index (0-100%).")
    ]

    html_flow = '<div style="margin-top: 15px;">'
    for num, title, desc in steps:
        html_flow += f"""
        <div class="flow-step">
            <div class="step-number">{num}</div>
            <div>
                <div class="step-content-title">{title}</div>
                <div class="step-content-desc">{desc}</div>
            </div>
        </div>
        """
    html_flow += '</div>'
    st.markdown(html_flow, unsafe_allow_html=True)

def generate_executive_html_report(res: dict, scenarios_df: pd.DataFrame) -> str:
    """
    Builds a standalone executive HTML report for download.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Reliance Retail What-If Simulator Executive Brief</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; margin: 0; }}
            .container {{ max-width: 900px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; }}
            h1 {{ color: #a78bfa; margin-top: 0; border-bottom: 2px solid #6366f1; padding-bottom: 12px; }}
            h2 {{ color: #c4b5fd; margin-top: 25px; }}
            .badge {{ background: #4f46e5; color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; }}
            th, td {{ border: 1px solid #334155; padding: 10px 14px; text-align: left; font-size: 13px; }}
            th {{ background: #312e81; color: #fff; }}
            .highlight {{ color: #10b981; font-weight: bold; }}
            .warning {{ color: #f59e0b; font-weight: bold; }}
            .danger {{ color: #ef4444; font-weight: bold; }}
            .footer {{ font-size: 11px; color: #94a3b8; margin-top: 30px; border-top: 1px solid #334155; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA</span>
            <h1>Reliance Retail What-If Simulator: Executive Brief</h1>
            <p><strong>Analysis Objective:</strong> Test whether a +{res['growth_target_pct']}% sales expansion is operationally feasible and profitable across staffing, inventory, warehousing, suppliers, and logistics.</p>
            <p><strong>Generated At:</strong> {now} | <strong>Horizon:</strong> {res['horizon_months']} Months | <strong>Feasibility Index:</strong> <span class="highlight">{res['feasibility_index']}% ({res['feasibility_status']})</span></p>

            <h2>1. Strategic Financial & Operational Summary</h2>
            <table>
                <tr><th>Metric</th><th>Scenario Realized</th><th>Baseline Benchmark</th><th>Incremental Variance</th></tr>
                <tr><td>Gross Realized Revenue</td><td>₹{res['realized_net_rev_cr']:,.2f} Cr</td><td>₹{res['baseline_total_rev_cr']:,.2f} Cr</td><td class="highlight">+₹{res['incremental_revenue_cr']:,.2f} Cr</td></tr>
                <tr><td>Operating Profit (EBITDA)</td><td>₹{res['ebitda_cr']:,.2f} Cr ({res['ebitda_margin_pct']}%)</td><td>₹{res['baseline_ebitda_cr']:,.2f} Cr ({res['baseline_ebitda_margin_pct']}%)</td><td class="highlight">+₹{res['incremental_ebitda_cr']:,.2f} Cr</td></tr>
                <tr><td>Customer Service SLA (OTIF)</td><td>{res['realized_otif_pct']}%</td><td>{res['baseline_otif_pct']}%</td><td>{round(res['realized_otif_pct'] - res['baseline_otif_pct'], 1)}%</td></tr>
                <tr><td>Working Capital Locked</td><td>₹{res['net_working_capital_locked_cr']:,.2f} Cr</td><td>-</td><td>Cash requirement for buffer stock</td></tr>
                <tr><td>Unmitigated Lost Sales</td><td>₹{res['lost_sales_cr']:,.2f} Cr</td><td>₹0.00 Cr</td><td>Revenue lost to bottlenecks</td></tr>
            </table>

            <h2>2. Operational Pillars Capacity Utilization</h2>
            <table>
                <tr><th>Capacity Pillar</th><th>Utilization %</th><th>Status Threshold</th></tr>
                {"".join([f"<tr><td>{k}</td><td>{v}%</td><td class='{'danger' if v>100 else ('warning' if v>85 else 'highlight')}'>{'BREACH (>100%)' if v>100 else ('STRAIN (85-100%)' if v>85 else 'BALANCED (<85%)')}</td></tr>" for k, v in res['pillar_utilizations'].items()])}
            </table>

            <h2>3. Comparative Scenarios Evaluation</h2>
            <table>
                <tr><th>Scenario</th><th>Feasibility</th><th>Net Rev (₹ Cr)</th><th>EBITDA (₹ Cr)</th><th>OTIF %</th><th>Lead Time</th></tr>
                {"".join([f"<tr><td>{row['Scenario']}</td><td>{row['Feasibility Score']}</td><td>₹{row['Net Revenue (₹ Cr)']:,.0f}</td><td>₹{row['EBITDA (₹ Cr)']:,.0f}</td><td>{row['OTIF Service %']}</td><td>{row['Lead Time']}</td></tr>" for _, row in scenarios_df.iterrows()])}
            </table>

            <h2>4. Executive Recommendations</h2>
            <ol>
                <li><strong>Pre-emptive Warehouse 2nd Shift:</strong> Regional distribution centers break first at +11% growth. Authorize 2nd shift activation across 8 regional hubs.</li>
                <li><strong>Elastic 3PL Surge Contracts:</strong> Secure on-demand delivery capacity with Delhivery/BlueDart for 25% flex volume to protect the 95% OTIF standard.</li>
                <li><strong>Seasonal Temp Staffing:</strong> Hire 14% temporary associates paired with cross-skilling certification to eliminate store front bottlenecks without permanent overhead inflation.</li>
                <li><strong>Working Capital Credit Facility:</strong> Arrange an ₹850-950 Cr revolving working capital credit line to fund 22 days of safety stock.</li>
            </ol>

            <div class="footer">
                Disclaimer: Built for business analytics and strategic capacity modeling prototyping. All figures and operational parameters are synthetic approximations.
            </div>
        </div>
    </body>
    </html>
    """
    return html

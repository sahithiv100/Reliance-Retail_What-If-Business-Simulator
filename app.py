"""
Reliance Retail What-If Business Simulator: Can Sales Grow 20%?
PROMPT 14 — Business Analytics Prototype
SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA. FOR ILLUSTRATIVE MODELING ONLY.

Authors: Senior Full-Stack Developer, Data Scientist & Product Designer
Stack: Python, Streamlit, Pandas, NumPy, Plotly
"""

import os
import sys

# Ensure root directory is always on sys.path regardless of where streamlit was launched
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import base64
from datetime import datetime

# Import modular components directly from root
from data_generator import generate_synthetic_data, save_synthetic_csvs, DEFAULT_SEED
from simulator_engine import SimulationEngine
from ui_components import (
    inject_custom_styles,
    render_top_banner,
    render_kpi_card,
    render_pillar_gauge,
    render_waterfall_pnl,
    render_bottleneck_heatmap,
    render_radar_comparison,
    render_monte_carlo_distribution,
    render_algorithm_flowchart,
    generate_executive_html_report,
    NAVY_BG, SURFACE_CARD, TEXT_PRIMARY, TEXT_MUTED, ACCENT_PURPLE,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER
)

# Set page config
st.set_page_config(
    page_title="Reliance Retail Simulator | Can Sales Grow 20%?",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
inject_custom_styles()

# -------------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------------
if "seed" not in st.session_state:
    st.session_state.seed = DEFAULT_SEED

if "synthetic_data" not in st.session_state:
    st.session_state.synthetic_data = generate_synthetic_data(st.session_state.seed)
    save_synthetic_csvs(st.session_state.synthetic_data)

if "growth_target_pct" not in st.session_state:
    st.session_state.growth_target_pct = 20.0

if "horizon_months" not in st.session_state:
    st.session_state.horizon_months = 3

if "mitigations" not in st.session_state:
    st.session_state.mitigations = {
        "overtime_pct_utilization": 10.0,
        "temp_hiring_pct": 14.0,
        "cross_skilling_enabled": True,
        "safety_stock_days": 22,
        "supplier_dual_sourcing_pct": 20.0,
        "supplier_reservation_fee_enabled": True,
        "warehouse_second_shift": True,
        "cross_docking_enabled": True,
        "third_party_3pl_flex_pct": 25.0
    }

# -------------------------------------------------------------
# Top Banner
# -------------------------------------------------------------
render_top_banner()

# Initialize Engine
engine = SimulationEngine(st.session_state.synthetic_data)

# -------------------------------------------------------------
# Sidebar Navigation & Scenario Controls
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Strategic Simulation Controls")

    # Quick Preset Buttons
    st.markdown("<p style='font-size:0.8rem; color:#94a3b8; margin-bottom:4px;'>STRATEGIC PRESETS</p>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("⚖️ Balanced (+20%)", use_container_width=True, help="Load recommended balanced operational expansion"):
            st.session_state.growth_target_pct = 20.0
            st.session_state.mitigations = {
                "overtime_pct_utilization": 10.0, "temp_hiring_pct": 14.0, "cross_skilling_enabled": True,
                "safety_stock_days": 22, "supplier_dual_sourcing_pct": 20.0, "supplier_reservation_fee_enabled": True,
                "warehouse_second_shift": True, "cross_docking_enabled": True, "third_party_3pl_flex_pct": 25.0
            }
            st.rerun()

    with col_p2:
        if st.button("⚠️ Unmitigated", use_container_width=True, help="Test raw +20% demand surge with zero operational action"):
            st.session_state.growth_target_pct = 20.0
            st.session_state.mitigations = {
                "overtime_pct_utilization": 0.0, "temp_hiring_pct": 0.0, "cross_skilling_enabled": False,
                "safety_stock_days": 16, "supplier_dual_sourcing_pct": 0.0, "supplier_reservation_fee_enabled": False,
                "warehouse_second_shift": False, "cross_docking_enabled": False, "third_party_3pl_flex_pct": 0.0
            }
            st.rerun()

    col_p3, col_p4 = st.columns(2)
    with col_p3:
        if st.button("🚚 Asset-Light", use_container_width=True, help="Load 3PL and temp staff flex strategy"):
            st.session_state.growth_target_pct = 20.0
            st.session_state.mitigations = {
                "overtime_pct_utilization": 8.0, "temp_hiring_pct": 22.0, "cross_skilling_enabled": False,
                "safety_stock_days": 20, "supplier_dual_sourcing_pct": 25.0, "supplier_reservation_fee_enabled": False,
                "warehouse_second_shift": False, "cross_docking_enabled": True, "third_party_3pl_flex_pct": 45.0
            }
            st.rerun()

    with col_p4:
        if st.button("🔄 Reset Baseline", use_container_width=True, help="Reset to 0% baseline"):
            st.session_state.growth_target_pct = 0.0
            st.session_state.mitigations = {
                "overtime_pct_utilization": 0.0, "temp_hiring_pct": 0.0, "cross_skilling_enabled": False,
                "safety_stock_days": 16, "supplier_dual_sourcing_pct": 0.0, "supplier_reservation_fee_enabled": False,
                "warehouse_second_shift": False, "cross_docking_enabled": False, "third_party_3pl_flex_pct": 0.0
            }
            st.rerun()

    st.markdown("---")

    # Primary Scenario Sliders
    growth_input = st.slider(
        "📈 Sales Growth Target (%)",
        min_value=-10.0,
        max_value=50.0,
        value=float(st.session_state.growth_target_pct),
        step=1.0,
        help="Target sales growth over the planning horizon. Default is +20%."
    )
    st.session_state.growth_target_pct = growth_input

    horizon_options = {
        1: "1 Month (Flash Sale / Festive Peak)",
        3: "3 Months (Quarterly Campaign)",
        6: "6 Months (H2 Strategic Plan)",
        12: "12 Months (Annual Operating Plan)"
    }
    horizon_input = st.selectbox(
        "⏱️ Planning Horizon",
        options=list(horizon_options.keys()),
        index=list(horizon_options.keys()).index(st.session_state.horizon_months),
        format_func=lambda x: horizon_options[x],
        help="Duration over which demand and operational capacity are simulated."
    )
    st.session_state.horizon_months = horizon_input

    st.markdown("---")
    st.markdown("### 🛠️ Operational Mitigation Levers")

    with st.expander("👥 1. Staffing & Labor Strategy", expanded=False):
        ot_input = st.slider(
            "Overtime Utilization (%)",
            min_value=0.0, max_value=20.0,
            value=float(st.session_state.mitigations.get("overtime_pct_utilization", 10.0)),
            step=1.0,
            help="Legal statutory limit is 20% overtime. Higher OT incurs 1.75x hourly wage premium."
        )
        st.session_state.mitigations["overtime_pct_utilization"] = ot_input

        temp_input = st.slider(
            "Seasonal Temp Staff Flex (%)",
            min_value=0.0, max_value=35.0,
            value=float(st.session_state.mitigations.get("temp_hiring_pct", 14.0)),
            step=1.0,
            help="Hires seasonal retail & warehouse associates (+15% wage, ₹15,000 onboarding cost)."
        )
        st.session_state.mitigations["temp_hiring_pct"] = temp_input

        cross_skill_input = st.checkbox(
            "Cross-Skilling Certification",
            value=bool(st.session_state.mitigations.get("cross_skilling_enabled", True)),
            help="Boosts frontline and fulfillment productivity by +10% through multi-role training."
        )
        st.session_state.mitigations["cross_skilling_enabled"] = cross_skill_input

    with st.expander("📦 2. Inventory & Working Capital", expanded=False):
        stock_days_input = st.slider(
            "Safety Stock Buffer (Days of Cover)",
            min_value=14, max_value=32,
            value=int(st.session_state.mitigations.get("safety_stock_days", 22)),
            step=1,
            help="Higher buffer protects against supplier stockouts but locks working capital."
        )
        st.session_state.mitigations["safety_stock_days"] = stock_days_input

    with st.expander("🏭 3. Suppliers & Procurement", expanded=False):
        dual_source_input = st.slider(
            "Secondary Dual-Sourcing Flex (%)",
            min_value=0.0, max_value=35.0,
            value=float(st.session_state.mitigations.get("supplier_dual_sourcing_pct", 20.0)),
            step=5.0,
            help="Routes overflow demand to certified secondary manufacturers (+7.5% surcharge)."
        )
        st.session_state.mitigations["supplier_dual_sourcing_pct"] = dual_source_input

        res_fee_input = st.checkbox(
            "Advance Capacity Reservation Fee",
            value=bool(st.session_state.mitigations.get("supplier_reservation_fee_enabled", True)),
            help="Pays 1.2% retainer to guarantee tier-1 suppliers reserve dedicated factory lines."
        )
        st.session_state.mitigations["supplier_reservation_fee_enabled"] = res_fee_input

    with st.expander("🏬 4. Warehousing & Fulfillment", expanded=False):
        wh_2nd_input = st.checkbox(
            "Activate 2nd / Night Shift at DCs",
            value=bool(st.session_state.mitigations.get("warehouse_second_shift", True)),
            help="Expands DC throughput by +40% with an 16% night shift wage allowance."
        )
        st.session_state.mitigations["warehouse_second_shift"] = wh_2nd_input

        cross_dock_input = st.checkbox(
            "Modular Cross-Docking Protocol",
            value=bool(st.session_state.mitigations.get("cross_docking_enabled", True)),
            help="Bypasses long-term pallet racking for fast-moving FMCG (+12% throughput speed)."
        )
        st.session_state.mitigations["cross_docking_enabled"] = cross_dock_input

    with st.expander("🚚 5. Logistics & Fleet Flex", expanded=False):
        tpl_input = st.slider(
            "Contracted 3PL Flex Allocation (%)",
            min_value=0.0, max_value=50.0,
            value=float(st.session_state.mitigations.get("third_party_3pl_flex_pct", 25.0)),
            step=5.0,
            help="Offloads overflow dispatches to Delhivery/BlueDart at on-demand peak rates."
        )
        st.session_state.mitigations["third_party_3pl_flex_pct"] = tpl_input

    st.markdown("---")
    st.markdown("### 🎲 Synthetic Data Controls")
    seed_input = st.number_input("Random Seed", value=int(st.session_state.seed), min_value=1, max_value=9999)
    if st.button("🔁 Regenerate Synthetic Dataset", use_container_width=True):
        st.session_state.seed = seed_input
        st.session_state.synthetic_data = generate_synthetic_data(seed_input)
        save_synthetic_csvs(st.session_state.synthetic_data)
        st.success(f"Regenerated synthetic dataset with seed {seed_input}!")
        st.rerun()

# -------------------------------------------------------------
# Execute Simulation Run for Active Controls
# -------------------------------------------------------------
sim_res = engine.run_simulation(
    growth_target_pct=st.session_state.growth_target_pct,
    horizon_months=st.session_state.horizon_months,
    mitigations=st.session_state.mitigations
)
scenarios_df = engine.generate_scenario_comparison(
    growth_target_pct=st.session_state.growth_target_pct,
    horizon_months=st.session_state.horizon_months
)

# -------------------------------------------------------------
# Main Application Header
# -------------------------------------------------------------
st.title("What-If Business Simulator: Can Sales Grow 20%?")
st.markdown(
    f"<p style='color:{TEXT_MUTED}; font-size:1.05rem; margin-top:-10px;'>"
    f"Illustrative Strategic Prototype for <b>Reliance Retail</b> &bull; "
    f"Simulating operational feasibility, capacity bottlenecks, working capital, and EBITDA across "
    f"<b>{st.session_state.growth_target_pct:+0.1f}% sales expansion</b> over a <b>{st.session_state.horizon_months}-month horizon</b>."
    f"</p>",
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# Navigation Tabs
# -------------------------------------------------------------
tab_exec, tab_deep, tab_sens, tab_manager, tab_data, tab_algo, tab_recs = st.tabs([
    "📊 Executive Simulator",
    "🔍 Departmental Deep Dive",
    "⚡ Sensitivity & Stress Test",
    "❓ Managerial Questions",
    "🗃️ Data Explorer",
    "⚙️ How the Algorithm Works",
    "📋 Strategic Action Plan"
])

# =============================================================
# TAB 1: EXECUTIVE SIMULATOR
# =============================================================
with tab_exec:
    # 1. Hero Status Card
    feas_color = sim_res["feasibility_color"]
    st.markdown(
        f"""
        <div style="background:{SURFACE_CARD}; border:2px solid {feas_color}; border-radius:12px; padding:18px 24px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="background:{feas_color}; color:#ffffff; font-size:0.75rem; font-weight:800; padding:4px 12px; border-radius:9999px; letter-spacing:0.8px;">
                    {sim_res['feasibility_status']}
                </span>
                <h2 style="color:{TEXT_PRIMARY}; margin:10px 0 4px 0; font-size:1.6rem;">
                    Feasibility Index: {sim_res['feasibility_index']} / 100
                </h2>
                <div style="color:{TEXT_MUTED}; font-size:0.88rem;">
                    Operational Risk Rating: <b style="color:{feas_color};">{sim_res['risk_level']}</b> &bull; 
                    Estimated Lead Time to Deploy: <b>{sim_res['lead_time_weeks']} Weeks</b>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="color:{TEXT_MUTED}; font-size:0.8rem; text-transform:uppercase;">Target Sales Growth</div>
                <div style="color:{TEXT_PRIMARY}; font-size:2.2rem; font-weight:800;">{sim_res['growth_target_pct']:+0.1f}%</div>
                <div style="color:{COLOR_SUCCESS}; font-size:0.82rem; font-weight:600;">{st.session_state.horizon_months}-Month Strategy</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Executive Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        rev_delta = f"+₹{sim_res['incremental_revenue_cr']:,.0f} Cr"
        render_kpi_card(
            title="Realized Net Revenue",
            value=f"₹{sim_res['realized_net_rev_cr']:,.0f} Cr",
            delta=rev_delta,
            delta_type="positive" if sim_res['incremental_revenue_cr'] >= 0 else "negative",
            subtitle=f"Target: ₹{sim_res['unconstrained_target_rev_cr']:,.0f} Cr (Lost: ₹{sim_res['lost_sales_cr']:,.0f} Cr)"
        )

    with m2:
        ebitda_delta = f"+₹{sim_res['incremental_ebitda_cr']:,.0f} Cr"
        render_kpi_card(
            title="Realized EBITDA",
            value=f"₹{sim_res['ebitda_cr']:,.0f} Cr",
            delta=f"{sim_res['ebitda_margin_pct']}% margin",
            delta_type="positive" if sim_res['ebitda_cr'] > sim_res['baseline_ebitda_cr'] else "negative",
            subtitle=f"Baseline: ₹{sim_res['baseline_ebitda_cr']:,.0f} Cr ({sim_res['baseline_ebitda_margin_pct']}%)"
        )

    with m3:
        otif_delta = f"{round(sim_res['realized_otif_pct'] - sim_res['baseline_otif_pct'], 1)}%"
        otif_type = "positive" if sim_res['realized_otif_pct'] >= 95.0 else ("neutral" if sim_res['realized_otif_pct'] >= 90.0 else "negative")
        render_kpi_card(
            title="Customer Service SLA (OTIF)",
            value=f"{sim_res['realized_otif_pct']}%",
            delta=otif_delta,
            delta_type=otif_type,
            subtitle="Gold Standard Target: ≥95.0% on-time"
        )

    with m4:
        render_kpi_card(
            title="Working Capital Cash Locked",
            value=f"₹{sim_res['net_working_capital_locked_cr']:,.0f} Cr",
            delta="Buffer Stock & Receivables",
            delta_type="neutral",
            subtitle=f"Inventory Buffer: ₹{sim_res['incremental_inventory_capital_cr']:,.0f} Cr"
        )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # 3. The 5 Capacity Pillars Gauges
    st.markdown("### 🎚️ Operational Capacity Utilization Across the 5 Pillars")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; margin-top:-8px;'>"
        f"Green: Balanced (&lt;85%) &bull; Amber: Operational Strain (85-100%) &bull; Red: Critical Bottleneck (&gt;100% Breached)"
        f"</p>",
        unsafe_allow_html=True
    )

    g1, g2, g3, g4, g5 = st.columns(5)
    with g1:
        st.plotly_chart(render_pillar_gauge("1. Staffing & Labor", sim_res["pillar_utilizations"]["Staffing & Labor"]), use_container_width=True)
    with g2:
        st.plotly_chart(render_pillar_gauge("2. Suppliers OEM", sim_res["pillar_utilizations"]["Supplier Capacity"]), use_container_width=True)
    with g3:
        st.plotly_chart(render_pillar_gauge("3. Warehouses DC", sim_res["pillar_utilizations"]["Warehouse Throughput"]), use_container_width=True)
    with g4:
        st.plotly_chart(render_pillar_gauge("4. Logistics Fleet", sim_res["pillar_utilizations"]["Logistics & Delivery"]), use_container_width=True)
    with g5:
        st.plotly_chart(render_pillar_gauge("5. Working Capital", sim_res["pillar_utilizations"]["Working Capital Buffer"], "140%"), use_container_width=True)

    # Bottleneck Breaches Alert
    breached_pillars = [k for k, v in sim_res["pillar_utilizations"].items() if v > 100.0]
    strained_pillars = [k for k, v in sim_res["pillar_utilizations"].items() if 85.0 < v <= 100.0]

    if breached_pillars:
        st.error(
            f"🚨 **CRITICAL CAPACITY BREACH DETECTED in {len(breached_pillars)} Pillar(s):** "
            f"**{', '.join(breached_pillars)}** exceeded 100% capacity. "
            f"Without additional mitigation, stockouts will trigger **₹{sim_res['lost_sales_cr']:,.0f} Cr in unfulfilled revenue** "
            f"and degrade customer OTIF to **{sim_res['realized_otif_pct']}%**."
        )
    elif strained_pillars:
        st.warning(
            f"⚠️ **OPERATIONAL STRAIN DETECTED in:** **{', '.join(strained_pillars)}**. "
            f"Capacity is operating between 85% and 100%. Buffer headroom is thin and vulnerable to demand surges."
        )
    else:
        st.success(
            f"✅ **ALL 5 PILLARS HEALTHY & BALANCED:** Operating within safe capacity thresholds (<85%). "
            f"Full demand is fulfilled with 96.2% OTIF service delivery."
        )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # 4. P&L Waterfall Bridge & Bottleneck Heatmap
    col_w, col_h = st.columns([6, 5])
    with col_w:
        st.plotly_chart(render_waterfall_pnl(sim_res), use_container_width=True)
    with col_h:
        st.plotly_chart(
            render_bottleneck_heatmap(
                st.session_state.synthetic_data["products_df"],
                st.session_state.synthetic_data["regions_df"],
                st.session_state.growth_target_pct
            ),
            use_container_width=True
        )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # 5. Comparative Scenarios Evaluation Table
    st.markdown("### 🏆 Strategic Scenario Comparison & Ranking")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; margin-top:-8px;'>"
        f"Comparing the current configuration against standard executive strategic options."
        f"</p>",
        unsafe_allow_html=True
    )

    col_tbl, col_rad = st.columns([7, 5])
    with col_tbl:
        st.dataframe(
            scenarios_df.style.apply(
                lambda row: [
                    'background-color: rgba(16, 185, 129, 0.15); font-weight: bold;' if "Recommended" in row["Scenario"]
                    else ('background-color: rgba(239, 68, 68, 0.15);' if "Unmitigated" in row["Scenario"] else '')
                    for _ in row
                ],
                axis=1
            ),
            use_container_width=True,
            hide_index=True
        )
    with col_rad:
        st.plotly_chart(render_radar_comparison(scenarios_df), use_container_width=True)

# =============================================================
# TAB 2: DEPARTMENTAL DEEP DIVE
# =============================================================
with tab_deep:
    st.markdown("## 🔍 Departmental Deep Dive: Capacity & Constraints")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.9rem; margin-top:-8px;'>"
        f"Examine granular operational metrics, capacity calculations, and cost structures across the 5 pillars."
        f"</p>",
        unsafe_allow_html=True
    )

    deep_tab1, deep_tab2, deep_tab3, deep_tab4, deep_tab5 = st.tabs([
        "👥 Workforce & Staffing",
        "🏭 Suppliers & Procurement",
        "🏬 Warehouses & DCs",
        "🚚 Logistics & Last-Mile",
        "📦 Inventory & Working Capital"
    ])

    with deep_tab1:
        st.markdown("### Frontline, Fulfillment & Courier Workforce")
        wf_details = sim_res["staffing_details"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Headcount Required", f"{wf_details['required_hours_month'] / 185:,.0f} Associates")
        c2.metric("Seasonal Temp Hires", f"+{wf_details['new_hires_needed']:,} Hires")
        c3.metric("Overtime Premium Cost", f"₹{sim_res['cost_breakdown']['Overtime Premium']:,.1f} Cr")
        c4.metric("Recruiting & Training Cost", f"₹{sim_res['cost_breakdown']['Temp Hiring & Training']:,.1f} Cr")

        st.markdown("#### Workforce Role Breakdown")
        st.dataframe(st.session_state.synthetic_data["workforce_df"], use_container_width=True, hide_index=True)

    with deep_tab2:
        st.markdown("### Supplier Network & Lead Time Management")
        sup_df = st.session_state.synthetic_data["suppliers_df"]
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Key Strategic Suppliers", f"{len(sup_df)} Suppliers")
        s2.metric("Supplier Capacity Headroom", f"+14.2% Burst")
        s3.metric("Expedite & Dual-Source Surcharges", f"₹{sim_res['cost_breakdown']['Supplier Expedite & Dual-Source']:,.1f} Cr")
        s4.metric("Capacity Reservation Fees", f"₹{sim_res['cost_breakdown']['Supplier Reservation Retainers']:,.1f} Cr")

        st.markdown("#### Strategic Supplier Portfolio (Sample of 64 Suppliers)")
        st.dataframe(sup_df.head(15), use_container_width=True, hide_index=True)

    with deep_tab3:
        st.markdown("### Mega Distribution Centers & Regional Hubs")
        wh_details = sim_res["warehouse_details"]
        w1, w2, w3, w4 = st.columns(4)
        w1.metric("Daily Units to Process", f"{wh_details['required_daily_units']:,.0f} Units/Day")
        w2.metric("DC Rated Daily Capacity", f"{wh_details['adjusted_max_daily_units']:,.0f} Units/Day")
        w3.metric("2nd Shift Premium Cost", f"₹{sim_res['cost_breakdown']['Warehouse 2nd Shift Surcharge']:,.1f} Cr")
        w4.metric("Handling Cost per Unit", "₹1.72 / unit")

        st.markdown("#### Regional Distribution Center Network")
        st.dataframe(st.session_state.synthetic_data["warehouses_df"], use_container_width=True, hide_index=True)

    with deep_tab4:
        st.markdown("### Dedicated Fleet & Elastic 3PL Logistics")
        log_details = sim_res["logistics_details"]
        l1, l2, l3, l4 = st.columns(4)
        l1.metric("Daily Dispatches Required", f"{log_details['required_daily_drops']:,.0f} Drops/Day")
        l2.metric("Owned Dedicated Drops", f"{log_details['owned_fleet_drops']:,.0f} Drops/Day")
        l3.metric("Contracted 3PL Overflow Drops", f"{log_details['tpl_drops']:,.0f} Drops/Day")
        l4.metric("3PL Flex Surcharge", f"₹{sim_res['cost_breakdown']['Logistics 3PL Flex Surcharge']:,.1f} Cr")

        st.markdown("#### Logistics Fleet Dispatch Channels")
        st.dataframe(st.session_state.synthetic_data["logistics_df"], use_container_width=True, hide_index=True)

    with deep_tab5:
        st.markdown("### Inventory Buffer Days & Working Capital Drain")
        i1, i2, i3, i4 = st.columns(4)
        i1.metric("Safety Stock Days of Cover", f"{st.session_state.mitigations['safety_stock_days']} Days")
        i2.metric("Incremental Buffer Capital", f"₹{sim_res['incremental_inventory_capital_cr']:,.1f} Cr")
        i3.metric("Annual Inventory Carrying Rate", "18.0% p.a.")
        i4.metric("Cost of Working Capital Financing", "10.5% p.a.")

        st.markdown(
            f"""
            <div class="content-box">
                <h4>Working Capital Cash Cycle Breakdown</h4>
                <ul>
                    <li><b>Days Sales Outstanding (DSO):</b> 7.0 Days (Rapid consumer cash & digital POS inflow)</li>
                    <li><b>Days Payable Outstanding (DPO):</b> 42.0 Days (Strategic vendor credit terms)</li>
                    <li><b>Net Working Capital Locked:</b> <b>₹{sim_res['net_working_capital_locked_cr']:,.1f} Crores</b></li>
                    <li><b>Financing Interest Cost:</b> ₹{sim_res['cost_breakdown']['Working Capital Financing']:,.1f} Crores</li>
                    <li><b>Inventory Holding / Shrinkage Cost:</b> ₹{sim_res['cost_breakdown']['Inventory Holding Cost']:,.1f} Crores</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

# =============================================================
# TAB 3: SENSITIVITY & STRESS TEST
# =============================================================
with tab_sens:
    st.markdown("## ⚡ Sensitivity Analysis & Monte Carlo Stress Testing")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.9rem; margin-top:-8px;'>"
        f"Multi-variable parameter sweeps and 1,000-iteration stochastic stress testing."
        f"</p>",
        unsafe_allow_html=True
    )

    st.markdown("### 1. 2D Sensitivity Matrix: Sales Growth Target vs Supplier Dual-Sourcing")
    sens_matrix = engine.run_2d_sensitivity_matrix(
        growth_range=[-10.0, 0.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0],
        supplier_flex_range=[0.0, 10.0, 20.0, 30.0],
        horizon_months=st.session_state.horizon_months
    )

    st.dataframe(
        sens_matrix.style.background_gradient(cmap="RdYlGn", vmin=30, vmax=98),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    st.markdown("### 2. Monte Carlo Stochastic Stress Test (1,000 Iterations)")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; margin-top:-8px;'>"
        f"Simulating random consumer demand volatility (±4.8%), supplier delivery lead time disruptions, and labor wage shocks."
        f"</p>",
        unsafe_allow_html=True
    )

    with st.spinner("Running 1,000 Monte Carlo iterations..."):
        mc_results = engine.run_monte_carlo_simulation(
            growth_target_pct=st.session_state.growth_target_pct,
            horizon_months=st.session_state.horizon_months,
            mitigations=st.session_state.mitigations,
            iterations=1000
        )

    # Display MC Percentiles
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        render_kpi_card("P10 Downside EBITDA", f"₹{mc_results['ebitda_p10']:,.0f} Cr", "90% Lower Floor", "negative", "Worst-case 10th percentile")
    with mc2:
        render_kpi_card("P50 Expected EBITDA", f"₹{mc_results['ebitda_p50']:,.0f} Cr", "Median Expected", "neutral", "50th percentile baseline")
    with mc3:
        render_kpi_card("P90 Upside EBITDA", f"₹{mc_results['ebitda_p90']:,.0f} Cr", "Favorable Upside", "positive", "Optimistic 90th percentile")
    with mc4:
        render_kpi_card("P10 Service SLA (OTIF)", f"{mc_results['otif_p10']}%", "Worst-case Floor", "neutral", "90% Confidence Lower SLA")

    st.plotly_chart(render_monte_carlo_distribution(mc_results), use_container_width=True)

# =============================================================
# TAB 4: MANAGERIAL QUESTIONS
# =============================================================
with tab_manager:
    st.markdown("## ❓ Key Managerial Questions Explored")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.9rem; margin-top:-8px;'>"
        f"Explore 4 critical executive dilemmas with calculated empirical findings, threshold points, and actionable decisions."
        f"</p>",
        unsafe_allow_html=True
    )

    manager_questions = engine.solve_manager_questions(st.session_state.horizon_months)

    for q in manager_questions:
        with st.container():
            st.markdown(
                f"""
                <div class="content-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="background:#4f46e5; color:#ffffff; font-weight:700; padding:3px 10px; border-radius:4px; font-size:0.75rem;">
                            EXECUTIVE QUERY {q['id']}
                        </span>
                        <span style="color:{COLOR_SUCCESS}; font-weight:700; font-size:0.85rem;">
                            {q['data_point']}
                        </span>
                    </div>
                    <h3 style="color:{TEXT_PRIMARY}; margin:4px 0 10px 0; font-size:1.15rem;">
                        {q['title']}
                    </h3>
                    <div style="background:#1e1b4b; border-left:4px solid #8b5cf6; padding:12px 16px; border-radius:4px; margin-bottom:12px;">
                        <b style="color:#c4b5fd;">VERDICT:</b> <span style="color:#ffffff;">{q['verdict']}</span>
                    </div>
                    <p style="color:{TEXT_MUTED}; font-size:0.9rem; line-height:1.5;">
                        <b>Analytical Finding:</b> {q['finding']}
                    </p>
                    <p style="color:#e0e7ff; font-size:0.9rem; line-height:1.5;">
                        <b>Strategic Recommendation:</b> {q['recommendation']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

# =============================================================
# TAB 5: DATA EXPLORER & DICTIONARY
# =============================================================
with tab_data:
    st.markdown("## 🗃️ Synthetic Data Explorer & Data Dictionary")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.9rem; margin-top:-8px;'>"
        f"Inspect all raw synthetic datasets generated for Reliance Retail. Filter by region or product category, and download CSVs."
        f"</p>",
        unsafe_allow_html=True
    )

    dataset_choice = st.selectbox(
        "Select Dataset to Preview & Download",
        options=[
            "Product Categories (products_df)",
            "Regional Zones (regions_df)",
            "Workforce Roles (workforce_df)",
            "Supplier Network (suppliers_df)",
            "Warehouses & DCs (warehouses_df)",
            "Logistics Dispatch Channels (logistics_df)"
        ]
    )

    data_map = {
        "Product Categories (products_df)": ("products_df", "synthetic_products_df.csv"),
        "Regional Zones (regions_df)": ("regions_df", "synthetic_regions_df.csv"),
        "Workforce Roles (workforce_df)": ("workforce_df", "synthetic_workforce_df.csv"),
        "Supplier Network (suppliers_df)": ("suppliers_df", "synthetic_suppliers_df.csv"),
        "Warehouses & DCs (warehouses_df)": ("warehouses_df", "synthetic_warehouses_df.csv"),
        "Logistics Dispatch Channels (logistics_df)": ("logistics_df", "synthetic_logistics_df.csv")
    }

    key, csv_name = data_map[dataset_choice]
    curr_df = st.session_state.synthetic_data[key]

    # Filters
    if key == "suppliers_df":
        cat_filter = st.multiselect("Filter by Product Category", options=curr_df["category_id"].unique(), default=curr_df["category_id"].unique())
        curr_df = curr_df[curr_df["category_id"].isin(cat_filter)]

    st.dataframe(curr_df, use_container_width=True, hide_index=True)

    # CSV Download Button
    csv_bytes = curr_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {csv_name}",
        data=csv_bytes,
        file_name=csv_name,
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### 📖 Comprehensive Data Dictionary")
    dict_data = [
        {"Table": "products_df", "Field": "baseline_monthly_units", "Type": "Integer", "Description": "Fictional monthly sales units at baseline for Reliance Retail nationwide stores."},
        {"Table": "products_df", "Field": "avg_unit_price_inr", "Type": "Float", "Description": "Average selling price per unit in Indian Rupees (INR)."},
        {"Table": "products_df", "Field": "gross_margin_pct", "Type": "Float", "Description": "Gross profit margin percentage (Revenue minus product acquisition cost)."},
        {"Table": "products_df", "Field": "max_supplier_burst_pct", "Type": "Float", "Description": "Maximum surge capacity primary manufacturers can deliver before experiencing a capacity cliff."},
        {"Table": "workforce_df", "Field": "standard_hours_per_worker_month", "Type": "Integer", "Description": "Contracted monthly regular working hours per employee (typically 180-190 hrs)."},
        {"Table": "workforce_df", "Field": "statutory_max_overtime_hours_month", "Type": "Integer", "Description": "Statutory legal overtime ceiling in India (max 30-36 hrs/month)."},
        {"Table": "suppliers_df", "Field": "standard_lead_time_days", "Type": "Integer", "Description": "Replenishment lead time in days under normal operating cadence."},
        {"Table": "warehouses_df", "Field": "maximum_rated_daily_units", "Type": "Integer", "Description": "Maximum units a distribution center can receive, pick, and dispatch in a 24-hr cycle."},
        {"Table": "logistics_df", "Field": "base_cost_per_drop_inr", "Type": "Float", "Description": "Direct delivery operating cost per dispatch drop in INR."}
    ]
    st.dataframe(pd.DataFrame(dict_data), use_container_width=True, hide_index=True)

# =============================================================
# TAB 6: HOW THE ALGORITHM WORKS
# =============================================================
with tab_algo:
    st.markdown("## ⚙️ How the Algorithm Works")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.9rem; margin-top:-8px;'>"
        f"A transparent, deterministic mathematical simulation engine connecting commercial demand to supply chain physics."
        f"</p>",
        unsafe_allow_html=True
    )

    render_algorithm_flowchart()

    st.markdown("---")
    st.markdown("### 📐 Mathematical Formulation & Capacity Equations")
    st.markdown(
        """
        #### 1. Labor Hours Translation
        $$\\text{Total Staff Hours Required} = \\frac{\\text{Baseline Standard Hours} \\times 0.835 \\times (1 + \\text{Growth\\%})}{\\text{Productivity Multiplier}}$$
        *Where $\\text{Productivity Multiplier} = 1.10$ if Cross-Skilling is enabled, and $1.0$ otherwise.*

        #### 2. Warehouse Throughput Constraint
        $$\\text{Warehouse Utilization} = \\frac{\\sum \\text{Daily Units Required}}{\\sum (\\text{DC Maximum Rated Capacity} \\times \\text{Shift Multiplier} \\times \\text{CrossDock Multiplier})}$$
        *Where 2nd Shift adds $+40\\%$ throughput, and Cross-Docking adds $+12\\%$.*

        #### 3. Working Capital Cash Drain
        $$\\Delta \\text{Cash Locked} = (\\text{Safety Stock Days} - \\text{Baseline Days}) \\times \\text{Daily COGS} + \\Delta \\text{AR} - \\Delta \\text{AP}$$
        *Where $\\Delta \\text{AR} = \\frac{\\Delta \\text{Sales}}{30} \\times 7\\text{ days DSO}$, and $\\Delta \\text{AP} = \\frac{\\Delta \\text{COGS}}{30} \\times 42\\text{ days DPO}$.*

        #### 4. Non-Linear Customer Service SLA (OTIF)
        $$\\text{Realized OTIF} = \\max\\left(62.0\\%, 96.2\\% - 1.25 \\times \\text{Supplier Deficit\\%} - 0.90 \\times \\text{WH Deficit\\%} - 0.95 \\times \\text{Logistics Deficit\\%} - 0.75 \\times \\text{Staff Deficit\\%}\\right)$$
        """
    )

    st.markdown("---")
    st.markdown("### ⚠️ Model Limitations & Boundary Disclosures")
    st.markdown(
        """
        - **Synthetic Calibration:** While calibrated to Reliance Retail's enterprise scale (~₹18,500 Cr/month revenue across 18,000 stores), all SKU numbers, supplier agreements, and regional margins are synthetic approximations.
        - **Static Cost Structure:** Fixed wage rates and logistics base tariffs are assumed constant over the horizon; severe macro-inflation is modeled via the Monte Carlo stress test tab.
        - **Human Review Safeguard:** High-impact human capital and operational capital expenditures must undergo managerial oversight. This tool does not execute automatic payroll or warehouse machinery operations.
        """
    )

# =============================================================
# TAB 7: STRATEGIC ACTION PLAN & REPORT
# =============================================================
with tab_recs:
    st.markdown("## 📋 Strategic Recommendations & Phased Action Plan")
    st.markdown(
        f"<p style='color:{TEXT_MUTED}; font-size:0.9rem; margin-top:-8px;'>"
        f"Prioritized operational interventions, risk governance checklists, and downloadable executive reports."
        f"</p>",
        unsafe_allow_html=True
    )

    recs_table = [
        {"Priority": "P1 (Critical)", "Intervention": "Activate 2nd Shift at Mega DCs", "Pillar": "Warehouses", "Evidence": "DC capacity breached at +11% growth", "Assumptions": "16% night shift wage premium", "EBITDA Impact": "+₹850 Cr (protects sales)", "Uncertainty": "Low", "Lead Time": "4 Weeks"},
        {"Priority": "P1 (Critical)", "Intervention": "Contract 3PL Flex Capacity (25%)", "Pillar": "Logistics", "Evidence": "Owned fleet capped at 1.35M drops/day", "Assumptions": "Contracted surge tariff ₹105/drop", "EBITDA Impact": "+₹420 Cr (avoids SLA drop)", "Uncertainty": "Low", "Lead Time": "2 Weeks"},
        {"Priority": "P2 (High)", "Intervention": "Seasonal Temp Staffing (+14%)", "Pillar": "Workforce", "Evidence": "Store queues cause cart abandonment", "Assumptions": "₹15k training cost, 88% ramp speed", "EBITDA Impact": "+₹380 Cr", "Uncertainty": "Medium", "Lead Time": "3 Weeks"},
        {"Priority": "P2 (High)", "Intervention": "Supplier Reservation Retainers", "Pillar": "Suppliers", "Evidence": "Tier-1 OEMs cap burst at +14%", "Assumptions": "1.2% reservation retainer", "EBITDA Impact": "+₹310 Cr", "Uncertainty": "Medium", "Lead Time": "4 Weeks"},
        {"Priority": "P3 (Medium)", "Intervention": "Expand Safety Stock to 22 Days", "Pillar": "Inventory", "Evidence": "Prevents stockouts during surge", "Assumptions": "10.5% cost of capital", "EBITDA Impact": "Net Cash: -₹360 Cr", "Uncertainty": "Low", "Lead Time": "3 Weeks"}
    ]
    st.dataframe(pd.DataFrame(recs_table), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🗓️ Phased 12-Week Implementation Roadmap")
    gantt_html = """
    <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:20px;">
        <div style="margin-bottom:12px;">
            <b style="color:#c4b5fd;">Phase 1: Weeks 1-4 (Rapid Surge Stabilization)</b>
            <div style="color:#94a3b8; font-size:0.85rem;">Execute 3PL on-demand logistics contracts &bull; Authorize 10% frontline overtime &bull; Initiate seasonal temporary hiring drive.</div>
        </div>
        <div style="margin-bottom:12px;">
            <b style="color:#818cf8;">Phase 2: Weeks 5-8 (Shift Expansion & Supplier Dual-Sourcing)</b>
            <div style="color:#94a3b8; font-size:0.85rem;">Ramp up 2nd / night shift across 8 mega-DCs &bull; Onboard certified secondary suppliers &bull; Roll out cross-skilling modules.</div>
        </div>
        <div>
            <b style="color:#38bdf8;">Phase 3: Weeks 9-12 (Resilience Buffering & Full Scale)</b>
            <div style="color:#94a3b8; font-size:0.85rem;">Scale inventory buffer to 22 days of cover &bull; Lock in supplier reservation agreements &bull; Audit OTIF service SLA.</div>
        </div>
    </div>
    """
    st.markdown(gantt_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📥 Download Executive Deliverables")

    html_report = generate_executive_html_report(sim_res, scenarios_df)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📄 Download Complete Executive Brief (HTML)",
            data=html_report,
            file_name=f"Reliance_Retail_Executive_Brief_{st.session_state.growth_target_pct:+0.0f}pct.html",
            mime="text/html",
            use_container_width=True
        )

    with col_d2:
        summary_md = f"""# Reliance Retail What-If Business Simulator Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Growth: {sim_res['growth_target_pct']:+0.1f}% | Horizon: {sim_res['horizon_months']} Months
Feasibility Score: {sim_res['feasibility_index']} / 100 ({sim_res['feasibility_status']})

## Financial Results
- Realized Net Revenue: ₹{sim_res['realized_net_rev_cr']:,.2f} Cr (Baseline: ₹{sim_res['baseline_total_rev_cr']:,.2f} Cr)
- Realized EBITDA: ₹{sim_res['ebitda_cr']:,.2f} Cr ({sim_res['ebitda_margin_pct']}%)
- Incremental EBITDA: ₹{sim_res['incremental_ebitda_cr']:,.2f} Cr
- Customer OTIF SLA: {sim_res['realized_otif_pct']}% (Baseline: 96.2%)
- Working Capital Locked: ₹{sim_res['net_working_capital_locked_cr']:,.2f} Cr

## Pillar Utilizations
{json.dumps(sim_res['pillar_utilizations'], indent=2)}
"""
        st.download_button(
            label="📝 Download Markdown Analysis Summary",
            data=summary_md,
            file_name=f"Reliance_Retail_Analysis_{st.session_state.growth_target_pct:+0.0f}pct.md",
            mime="text/markdown",
            use_container_width=True
        )

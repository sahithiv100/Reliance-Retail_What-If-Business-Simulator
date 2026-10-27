# 🏬 What-If Business Simulator: Can Sales Grow 20%?
### Illustrative Strategic Prototype for **Reliance Retail**
> **SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA. FOR ILLUSTRATIVE MODELING & ACADEMIC/STRATEGIC SIMULATION ONLY.**

---

## 📌 Executive Summary & Business Objective
This interactive Business Analytics Simulator tests whether a **+20% sales expansion** is operationally feasible and profitable for an enterprise retail conglomerate (modeled after **Reliance Retail**, India's largest retail network across grocery, electronics, fashion, and omni-channel commerce).

When commercial teams target aggressive growth, the critical bottleneck is rarely customer demand—it is the **underlying supply chain physics**:
1. **Frontline & Fulfillment Staffing:** Store customer checkout queues, warehouse picking teams, and last-mile delivery riders face severe capacity strain and overtime caps.
2. **Supplier Production Capacity:** Tier-1 manufacturer factory burst limits, component shortages, and replenishment lead time variance create stockout risks.
3. **Mega Distribution Center Throughput:** Inbound dock congestion, pallet staging limits, and dispatch line bottlenecks.
4. **Logistics & Last-Mile Delivery:** Dedicated fleet limits versus elastic on-demand 3PL logistics networks.
5. **Working Capital & Cash Flow:** The liquidity drain of funding buffer safety stock before customer receivables and vendor payables settle.

This web application translates commercial targets into operational requirements across all 5 pillars, pinpoints the earliest breaking point, evaluates operational mitigation levers, and ranks strategic scenarios.

---

## 🏗️ Architecture & Root-Level File Structure
In strict compliance with deployment guidelines, all application logic, datasets, and configuration files reside directly in the root project directory without subfolders, ensuring zero path errors on **GitHub** and **Streamlit Community Cloud**:

```
reliance_retail_whatif_simulator/
├── app.py                     # Streamlit web app entrypoint, navigation, and reactive layout
├── simulator_engine.py        # Core mathematical engine, 5-pillar capacity modeling, P&L bridge, Monte Carlo
├── data_generator.py          # Synthetic dataset generator with reproducible seed control
├── ui_components.py           # Custom dark navy CSS, Plotly gauges, waterfall, radar, HTML report generator
├── requirements.txt           # Python dependencies (Streamlit, Pandas, NumPy, Plotly, SciPy)
├── synthetic_products_df.csv  # Pre-generated synthetic product category data
├── synthetic_regions_df.csv   # Pre-generated regional footprint data
├── synthetic_workforce_df.csv # Pre-generated workforce and wage data
├── synthetic_suppliers_df.csv # Pre-generated strategic supplier portfolio
├── synthetic_warehouses_df.csv# Pre-generated distribution center throughput data
├── synthetic_logistics_df.csv # Pre-generated logistics dispatch channels data
└── README.md                  # Comprehensive documentation and Windows run guide
```

---

## 🚀 Setup & Launch Instructions (Windows-Friendly)

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Navigate to Project Directory
Open PowerShell or Command Prompt:
```powershell
cd C:\Users\DELL\.gemini\antigravity\scratch\reliance_retail_whatif_simulator
```

### 3. Create a Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If running under Command Prompt `cmd.exe`, run `venv\Scripts\activate.bat`)*

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Launch the Streamlit App
```powershell
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🎛️ Key Interactive Features & Tabs

### 1. 📊 Executive Simulator
- **Hero Feasibility Card:** Instant status banner showing the **Feasibility Index (0-100%)**, operational risk rating, and deployment lead time.
- **Key Financial & Operational Metrics:** Realized Net Revenue, Realized EBITDA, Gross Margin %, Lost Sales due to stockouts, Working Capital Locked, and Customer Service OTIF SLA.
- **5 Pillar Capacity Gauges:** High-contrast Plotly gauges with visual green (<85%), amber (85-100%), and red (>100% breach) safety zones.
- **Bottleneck Breaches Scanner:** Real-time scanner identifying which pillar breaks and calculating the exact revenue loss from stockouts.
- **EBITDA Waterfall Bridge:** Interactive Plotly waterfall decomposing baseline earnings into revenue expansion, overtime costs, 2nd shift allowances, 3PL surcharges, holding costs, and realized EBITDA.
- **Scenario Comparison Matrix & Radar:** Live comparison of 6 operational bundles:
  1. *Baseline Status Quo (0% Growth)*
  2. *Unmitigated Rush (+20% No Action)*
  3. *Lean Overtime Only*
  4. *Asset-Light 3PL & Temp Flex*
  5. *Balanced Operational Scaling (Recommended)*
  6. *High Buffer / Max Resilience*

### 2. 🔍 Departmental Deep Dive
Granular breakdown with individual interactive tabs for:
- **Workforce & Staffing:** Required associate hours, regular vs overtime vs temp hours, wage costs, recruitment lead time, and skill sets.
- **Suppliers & Procurement:** Supplier portfolio (64 suppliers), lead time shifts, expedite fees, and dual-sourcing allocation.
- **Warehouses & DCs:** 8 regional logistics parks (Bhiwandi, Sanand, Farrukhnagar, Dadri, Bengaluru, Hyderabad, Dankuni, Cuttack), daily throughput, dock doors, and 2nd shift activation.
- **Logistics & Delivery:** Owned dedicated van fleet, hyperlocal 2W couriers, and on-demand contracted 3PL elastic surge.
- **Inventory & Working Capital:** Safety stock days of cover (14-32 days), inventory valuation, accounts receivable (7d DSO) vs payable credit terms (42d DPO), and capital financing interest.

### 3. ⚡ Sensitivity Analysis & Monte Carlo Stress Testing
- **2D Sensitivity Matrix:** Parameter sweeps across Growth Target (-10% to +40%) vs Supplier Dual-Sourcing headroom.
- **Monte Carlo Simulation (1,000 Iterations):** Stochastic model introducing normal demand volatility (±4.8%), gamma supplier delays, and wage shocks. Displays P10 (Downside), P50 (Median), and P90 (Upside) confidence intervals and Value-at-Risk (VaR).

### 4. ❓ Managerial Questions Explorer
Dedicated computational modules solving 4 practical executive questions:
1. *Can Reliance Retail absorb a +20% festive rush with existing store and warehouse staff?* (Verdict: NO — severe staff deficit and OTIF drop to 81.5%).
2. *Which supply chain pillar breaks first, and at what exact sales threshold?* (Verdict: Mega DC throughput breaches at +11%, Suppliers at +14%, Logistics at +16%).
3. *What is the net working capital required to support +20% growth without stockouts?* (Verdict: ₹360-450 Cr net cash injection required for 22 days safety stock).
4. *Speed vs Margin Trade-off: 4-week rapid sprint vs 12-week structural expansion?* (Verdict: Rapid sprint achieves 92.4% OTIF with 0.8% margin compression; 12-week plan achieves 96.2% OTIF and maximizes profit).

### 5. 🗃️ Data Explorer & Data Dictionary
- Interactive data table previews with filtering by product category and geographic zone.
- Comprehensive Data Dictionary detailing every column, data type, and business definition.
- One-click CSV downloads for all synthetic tables.

### 6. ⚙️ How the Algorithm Works
- Connected 7-stage visual flow explaining demand scaling, capacity translation, constraint checking, OTIF penalties, and P&L bridging.
- Transparent mathematical equations for labor hours, DC throughput, working capital cash drain, and non-linear customer service degradation.
- Explicit disclosures of model limitations and boundary assumptions.

### 7. 📋 Strategic Recommendations & Action Plan
- Structured recommendations matrix detailing Action, Pillar, Priority, Evidence, Assumptions, Expected EBITDA Impact, Uncertainty Level, and Lead Time.
- Phased 12-week implementation roadmap across 3 strategic phases.
- AI Governance & Human-in-the-Loop Safeguards (strict human review required for capital allocation and workforce decisions).
- Downloadable Executive HTML Report and Markdown Brief.

---

## 🎨 Design & Styling Tokens
- **Theme:** Professional dark navy/charcoal interface with restrained purple accents (`#8b5cf6`, `#7c3aed`, `#6366f1`).
- **Typography:** Modern clean system typography (Inter / SF Pro / Segoe UI) with crisp hierarchy and legible contrast.
- **Visual Feedback:** Color-coded status pills, real-time reactive sliders, informative hover tooltips, and clear delta indicators.

---

## 🛡️ Synthetic Data Notice & Disclaimer
All data, product volumes, supplier lists, warehouse throughput ratings, and financials are **synthetic approximations** created solely for business analytics modeling and strategic prototyping. This application does not scrape or reflect proprietary company databases, and does not automate adverse HR decisions or industrial equipment.

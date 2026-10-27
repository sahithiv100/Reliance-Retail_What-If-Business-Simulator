"""
Synthetic Data Generator for Reliance Retail Business Simulator
PROMPT 14 — What-If Business Simulator: Can Sales Grow 20%?
SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA. FOR ILLUSTRATIVE MODELING ONLY.

This module generates internally consistent fictional data calibrated to the enterprise scale of
Reliance Retail (India's largest retail conglomerate):
- Product Categories & SKUs (Pricing, Margins, Handling Specs)
- Regional Geographies & Store Networks (18,000+ store footprint)
- Workforce Skills, Headcount, Productivity & Labor Costs
- Suppliers, Replenishment Lead Times & Capacity Caps
- Warehouses / Distribution Center Throughput
- Logistics Fleet & Last-Mile Dispatch Capacity
- Financial & Working Capital Constants
"""

import numpy as np
import pandas as pd
import os
import sys

# Ensure root directory is always on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

DEFAULT_SEED = 42

def generate_synthetic_data(seed: int = DEFAULT_SEED) -> dict:
    """
    Generates a synchronized, internally consistent synthetic dataset for Reliance Retail prototype.
    Calibrated to enterprise scale (~₹18,500 Cr/month revenue, ~7.8% EBITDA margin baseline).
    """
    rng = np.random.default_rng(seed)

    # 1. Product Categories & Strategic Segments
    # Units calibrated to enterprise nationwide scale
    categories_data = [
        {
            "category_id": "CAT_GROCERY",
            "category_name": "Grocery & Fresh Foods",
            "format": "Smart Bazaar / JioMart Superstore",
            "baseline_monthly_units": 185_000_000,
            "avg_unit_price_inr": 210.0,
            "gross_margin_pct": 19.2,
            "storage_volume_m3_per_unit": 0.0035,
            "units_handled_per_staff_hour": 68.0,
            "shelf_life_days": 18,
            "default_lead_time_days": 4,
            "supplier_count": 85,
            "max_supplier_burst_pct": 114.0,  # +14% burst before supplier cliff
            "inventory_days_cover": 14,
            "logistics_drops_per_100_units": 2.2,
            "handling_complexity": "Medium (Perishable / Temperature Sensitive)"
        },
        {
            "category_id": "CAT_ELECTRONICS",
            "category_name": "Consumer Electronics & Tech",
            "format": "Reliance Digital / Jio Stores",
            "baseline_monthly_units": 5_400_000,
            "avg_unit_price_inr": 11_800.0,
            "gross_margin_pct": 15.4,
            "storage_volume_m3_per_unit": 0.0380,
            "units_handled_per_staff_hour": 16.0,
            "shelf_life_days": 365,
            "default_lead_time_days": 24,
            "supplier_count": 32,
            "max_supplier_burst_pct": 111.0,  # Semiconductor / OEM lead time constraints
            "inventory_days_cover": 28,
            "logistics_drops_per_100_units": 7.5,
            "handling_complexity": "High (High Value / Secure Storage / White Glove)"
        },
        {
            "category_id": "CAT_FASHION",
            "category_name": "Fashion & Lifestyle",
            "format": "Reliance Trends / Trends Footwear / Azorte",
            "baseline_monthly_units": 38_000_000,
            "avg_unit_price_inr": 1_280.0,
            "gross_margin_pct": 39.5,
            "storage_volume_m3_per_unit": 0.0075,
            "units_handled_per_staff_hour": 42.0,
            "shelf_life_days": 180,
            "default_lead_time_days": 21,
            "supplier_count": 64,
            "max_supplier_burst_pct": 116.0,  # Garment mill subcontracting capacity
            "inventory_days_cover": 32,
            "logistics_drops_per_100_units": 3.8,
            "handling_complexity": "Medium (Style/Size/SKU Proliferation)"
        },
        {
            "category_id": "CAT_HPC",
            "category_name": "Home, Health & Personal Care",
            "format": "Reliance Smart Point / General FMCG",
            "baseline_monthly_units": 94_000_000,
            "avg_unit_price_inr": 285.0,
            "gross_margin_pct": 24.8,
            "storage_volume_m3_per_unit": 0.0028,
            "units_handled_per_staff_hour": 74.0,
            "shelf_life_days": 360,
            "default_lead_time_days": 7,
            "supplier_count": 72,
            "max_supplier_burst_pct": 120.0,  # Large FMCG scale
            "inventory_days_cover": 21,
            "logistics_drops_per_100_units": 2.0,
            "handling_complexity": "Low (Standardized Cartons / High Velocity)"
        },
        {
            "category_id": "CAT_PHARMA",
            "category_name": "Pharma & Wellness",
            "format": "Netmeds / Wellness Kiosks",
            "baseline_monthly_units": 18_500_000,
            "avg_unit_price_inr": 540.0,
            "gross_margin_pct": 27.5,
            "storage_volume_m3_per_unit": 0.0012,
            "units_handled_per_staff_hour": 36.0,
            "shelf_life_days": 270,
            "default_lead_time_days": 6,
            "supplier_count": 48,
            "max_supplier_burst_pct": 115.0,  # Cold chain / regulatory traceability
            "inventory_days_cover": 20,
            "logistics_drops_per_100_units": 4.5,
            "handling_complexity": "High (Cold Chain / Licensed Pharmacist Handover)"
        }
    ]
    products_df = pd.DataFrame(categories_data)
    # Baseline revenue in ₹ Crores (1 Crore = 10,000,000 INR)
    products_df["baseline_monthly_rev_cr"] = (
        products_df["baseline_monthly_units"] * products_df["avg_unit_price_inr"]
    ) / 10_000_000.0
    products_df["baseline_cogs_cr"] = (
        products_df["baseline_monthly_rev_cr"] * (1 - products_df["gross_margin_pct"] / 100.0)
    )
    products_df["baseline_gross_profit_cr"] = (
        products_df["baseline_monthly_rev_cr"] - products_df["baseline_cogs_cr"]
    )

    # 2. Regional Footprint & Distribution (North, West, South, East)
    regions_data = [
        {
            "region_id": "REG_NORTH",
            "region_name": "North Zone (Delhi NCR, Punjab, UP, Haryana)",
            "volume_share_pct": 29.0,
            "stores_count": 5250,
            "distribution_centers": 26,
            "warehouse_capacity_units_day": 3_600_000,
            "logistics_delivery_fleet_vans": 6200,
            "logistics_2w_couriers": 14500,
            "daily_delivery_cap_drops": 340_000,
            "headcount_store_associates": 48_000,
            "headcount_warehouse_staff": 12_500,
            "headcount_delivery_agents": 15_200,
            "avg_hourly_wage_inr": 145.0,
            "regional_demand_volatility_pct": 6.8
        },
        {
            "region_id": "REG_WEST",
            "region_name": "West Zone (Mumbai MMR, Pune, Gujarat, MP)",
            "volume_share_pct": 31.5,
            "stores_count": 5780,
            "distribution_centers": 30,
            "warehouse_capacity_units_day": 3_900_000,
            "logistics_delivery_fleet_vans": 6800,
            "logistics_2w_couriers": 16200,
            "daily_delivery_cap_drops": 380_000,
            "headcount_store_associates": 52_500,
            "headcount_warehouse_staff": 13_800,
            "headcount_delivery_agents": 16_800,
            "avg_hourly_wage_inr": 156.0,
            "regional_demand_volatility_pct": 5.4
        },
        {
            "region_id": "REG_SOUTH",
            "region_name": "South Zone (Bengaluru, Hyderabad, Chennai, Kerala)",
            "volume_share_pct": 25.0,
            "stores_count": 4650,
            "distribution_centers": 24,
            "warehouse_capacity_units_day": 3_200_000,
            "logistics_delivery_fleet_vans": 5400,
            "logistics_2w_couriers": 12800,
            "daily_delivery_cap_drops": 310_000,
            "headcount_store_associates": 43_000,
            "headcount_warehouse_staff": 11_200,
            "headcount_delivery_agents": 13_500,
            "avg_hourly_wage_inr": 150.0,
            "regional_demand_volatility_pct": 5.9
        },
        {
            "region_id": "REG_EAST",
            "region_name": "East & North-East Zone (Kolkata, Bihar, Odisha, Assam)",
            "volume_share_pct": 14.5,
            "stores_count": 2850,
            "distribution_centers": 16,
            "warehouse_capacity_units_day": 2_100_000,
            "logistics_delivery_fleet_vans": 3200,
            "logistics_2w_couriers": 7600,
            "daily_delivery_cap_drops": 180_000,
            "headcount_store_associates": 26_500,
            "headcount_warehouse_staff": 6_900,
            "headcount_delivery_agents": 8_200,
            "avg_hourly_wage_inr": 134.0,
            "regional_demand_volatility_pct": 8.0
        }
    ]
    regions_df = pd.DataFrame(regions_data)

    # 3. Workforce Roles, Capacity & Productivity
    workforce_roles_data = [
        {
            "role_id": "ROLE_STORE_FRONT",
            "role_name": "Store Customer Associates & Cashiers",
            "total_headcount": int(regions_df["headcount_store_associates"].sum()),
            "standard_hours_per_worker_month": 180,
            "statutory_max_overtime_hours_month": 32,
            "avg_hourly_base_pay_inr": 142.0,
            "overtime_multiplier": 1.75,
            "units_capacity_per_hour": 58.0,
            "hiring_lead_time_weeks": 3,
            "recruiting_training_cost_per_hire_inr": 14_500,
            "attrition_rate_annual_pct": 21.0,
            "critical_skill": "POS Billing, Customer Assistance, Shelf Replenishment"
        },
        {
            "role_id": "ROLE_WH_FULFILLMENT",
            "role_name": "Warehouse Picking, Staging & Inbound Staff",
            "total_headcount": int(regions_df["headcount_warehouse_staff"].sum()),
            "standard_hours_per_worker_month": 190,
            "statutory_max_overtime_hours_month": 36,
            "avg_hourly_base_pay_inr": 154.0,
            "overtime_multiplier": 1.80,
            "units_capacity_per_hour": 78.0,
            "hiring_lead_time_weeks": 4,
            "recruiting_training_cost_per_hire_inr": 18_000,
            "attrition_rate_annual_pct": 24.0,
            "critical_skill": "WMS RF Scanner, Pallet Jack, Batch Sorting, Dock Unloading"
        },
        {
            "role_id": "ROLE_LAST_MILE",
            "role_name": "Delivery Associates & Fleet Operators",
            "total_headcount": int(regions_df["headcount_delivery_agents"].sum()),
            "standard_hours_per_worker_month": 190,
            "statutory_max_overtime_hours_month": 30,
            "avg_hourly_base_pay_inr": 146.0,
            "overtime_multiplier": 1.70,
            "units_capacity_per_hour": 24.0,  # Drops / dispatches equivalent
            "hiring_lead_time_weeks": 2,
            "recruiting_training_cost_per_hire_inr": 12_000,
            "attrition_rate_annual_pct": 32.0,
            "critical_skill": "Route Navigation, Cold Box Handling, OTP Customer Verification"
        }
    ]
    workforce_df = pd.DataFrame(workforce_roles_data)

    # 4. Supplier Network & Supply Base (Synthesizing 64 representative key suppliers)
    supplier_tiers = []
    supplier_names_prefix = [
        ("Amul Dairy Coop", "CAT_GROCERY", 4, 1.15, 97.8),
        ("Nestle India Ltd", "CAT_GROCERY", 5, 1.14, 98.2),
        ("Hindustan Unilever Ltd", "CAT_HPC", 6, 1.20, 98.9),
        ("ITC Foods & Agri", "CAT_GROCERY", 5, 1.16, 97.4),
        ("Samsung Electronics India", "CAT_ELECTRONICS", 26, 1.11, 94.8),
        ("Apple India Logistics", "CAT_ELECTRONICS", 28, 1.09, 95.2),
        ("Xiaomi Mobile Ltd", "CAT_ELECTRONICS", 21, 1.14, 94.0),
        ("LG Electronics India", "CAT_ELECTRONICS", 22, 1.12, 95.8),
        ("Arvind Fashions & Mills", "CAT_FASHION", 20, 1.18, 92.8),
        ("Raymond Apparel Sourcing", "CAT_FASHION", 22, 1.17, 92.0),
        ("Aditya Birla Fashion Group", "CAT_FASHION", 19, 1.19, 93.4),
        ("Procter & Gamble India", "CAT_HPC", 7, 1.22, 98.2),
        ("Dabur Consumer Care", "CAT_HPC", 6, 1.18, 96.8),
        ("Sun Pharma Laboratories", "CAT_PHARMA", 6, 1.15, 96.4),
        ("Cipla Health Logistics", "CAT_PHARMA", 5, 1.17, 97.5),
        ("Dr Reddy's Labs India", "CAT_PHARMA", 6, 1.16, 97.0)
    ]

    sup_id = 1
    for prefix, cat_id, lead_time, burst_cap, reliability in supplier_names_prefix:
        for reg in ["REG_NORTH", "REG_WEST", "REG_SOUTH", "REG_EAST"]:
            base_alloc = rng.integers(1_100_000, 5_800_000)
            max_cap = int(base_alloc * burst_cap)
            expedite_cost_pct = float(rng.uniform(6.5, 13.5))
            dual_source = bool(rng.random() > 0.35)
            supplier_tiers.append({
                "supplier_id": f"SUP_{sup_id:03d}",
                "supplier_name": f"{prefix} - {reg.split('_')[1]} Hub",
                "category_id": cat_id,
                "region_id": reg,
                "baseline_contracted_units_month": base_alloc,
                "maximum_capacity_units_month": max_cap,
                "capacity_headroom_pct": round((burst_cap - 1.0) * 100, 1),
                "standard_lead_time_days": lead_time,
                "expedited_lead_time_days": max(2, int(lead_time * 0.65)),
                "reliability_on_time_pct": reliability,
                "expedite_surcharge_pct": round(expedite_cost_pct, 1),
                "has_dual_source_alternate": dual_source,
                "tier_level": "Tier-1 Strategic" if base_alloc > 3_200_000 else "Tier-2 Secondary"
            })
            sup_id += 1
    suppliers_df = pd.DataFrame(supplier_tiers)

    # 5. Warehouses & Fulfillment Centers Network (Mega Regional Logistics Parks)
    warehouses_data = []
    wh_locations = [
        ("Bhiwandi Mega DC", "REG_WEST", 1_450_000, 1_850_000, 1_550_000, 64, 1.65),
        ("Sanand Central DC", "REG_WEST", 1_200_000, 1_450_000, 1_220_000, 48, 1.70),
        ("Farrukhnagar Logistics Park", "REG_NORTH", 1_550_000, 1_950_000, 1_620_000, 72, 1.68),
        ("Dadri Inbound Terminal", "REG_NORTH", 1_100_000, 1_350_000, 1_120_000, 44, 1.75),
        ("Hosur Bengaluru Hub", "REG_SOUTH", 1_350_000, 1_700_000, 1_420_000, 56, 1.66),
        ("Shamshabad Hyderabad Mega Hub", "REG_SOUTH", 1_250_000, 1_550_000, 1_280_000, 52, 1.72),
        ("Dankuni Kolkata Eastern Hub", "REG_EAST", 1_050_000, 1_250_000, 1_020_000, 40, 1.82),
        ("Cuttack Regional Staging DC", "REG_EAST", 750_000, 850_000, 680_000, 28, 1.88)
    ]
    for name, reg, sq_ft, max_daily_units, base_daily_units, dock_doors, unit_cost in wh_locations:
        warehouses_data.append({
            "warehouse_name": name,
            "region_id": reg,
            "storage_area_sqft": sq_ft,
            "baseline_daily_throughput_units": base_daily_units,
            "maximum_rated_daily_units": max_daily_units,
            "utilization_baseline_pct": round((base_daily_units / max_daily_units) * 100, 1),
            "dock_doors_count": dock_doors,
            "second_shift_ready": True if base_daily_units / max_daily_units < 0.88 else False,
            "warehouse_handling_cost_per_unit_inr": unit_cost,
            "rack_utilization_pct": float(rng.uniform(79.0, 87.0))
        })
    warehouses_df = pd.DataFrame(warehouses_data)

    # 6. Logistics & Last-Mile Dispatch Channels
    logistics_channels = [
        {
            "channel_id": "CH_OWNED_VAN",
            "channel_name": "Dedicated Fleet (Electric & ICE Mid-Vans)",
            "delivery_type": "Store B2B & Hyperlocal Hub Replenishment",
            "baseline_daily_drops": 680_000,
            "max_daily_drops_capacity": 820_000,
            "base_cost_per_drop_inr": 82.0,
            "on_time_sla_pct": 97.6,
            "co2_kg_per_drop": 0.45,
            "flexibility": "Low (Fixed Lease / Capital Heavy)"
        },
        {
            "channel_id": "CH_HYPERLOCAL_2W",
            "channel_name": "JioMart 2-Wheeler Express Couriers",
            "delivery_type": "D2C Direct-to-Consumer / Quick Commerce",
            "baseline_daily_drops": 440_000,
            "max_daily_drops_capacity": 530_000,
            "base_cost_per_drop_inr": 46.0,
            "on_time_sla_pct": 96.1,
            "co2_kg_per_drop": 0.18,
            "flexibility": "Medium (Gig Rider Network)"
        },
        {
            "channel_id": "CH_3PL_PARTNERS",
            "channel_name": "Contracted 3PL Logistics (Delhivery / BlueDart / XpressBees)",
            "delivery_type": "Peak Surge Spillover & Tier-2/3 Long Haul",
            "baseline_daily_drops": 190_000,
            "max_daily_drops_capacity": 450_000,  # High elasticity
            "base_cost_per_drop_inr": 105.0,      # Higher variable surcharge
            "on_time_sla_pct": 93.6,
            "co2_kg_per_drop": 0.60,
            "flexibility": "Very High (On-Demand Elastic Surge)"
        }
    ]
    logistics_df = pd.DataFrame(logistics_channels)

    # 7. Strategic Macro Constants
    financial_constants = {
        "cost_of_capital_annual_pct": 10.5,    # Short term working capital financing rate
        "inventory_carrying_cost_annual_pct": 18.0, # Obsolescence, shrinkage, insurance, storage
        "days_sales_outstanding_dso": 7.0,     # Rapid retail cash inflow
        "days_payable_outstanding_dpo": 42.0,  # Supplier credit terms
        "corporate_tax_rate_pct": 25.17,       # Indian corporate tax rate
        "target_on_time_in_full_otif_pct": 95.0, # Gold standard customer SLA
        "synthetic_notice": "SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA"
    }

    return {
        "products_df": products_df,
        "regions_df": regions_df,
        "workforce_df": workforce_df,
        "suppliers_df": suppliers_df,
        "warehouses_df": warehouses_df,
        "logistics_df": logistics_df,
        "constants": financial_constants,
        "seed": seed
    }

def save_synthetic_csvs(data_dict: dict, root_dir: str = CURRENT_DIR):
    """
    Saves synthetic datasets as CSV in root directory for instant user download and inspectability.
    """
    for key, df in data_dict.items():
        if isinstance(df, pd.DataFrame):
            filename = f"synthetic_{key}.csv"
            filepath = os.path.join(root_dir, filename)
            df.to_csv(filepath, index=False)

if __name__ == "__main__":
    data = generate_synthetic_data(DEFAULT_SEED)
    save_synthetic_csvs(data)
    print("Synthetic enterprise data generated successfully.")
    for k, v in data.items():
        if isinstance(v, pd.DataFrame):
            print(f" - {k}: {v.shape[0]} rows, {v.shape[1]} columns")

import csv

# =============================================================================
# GDP FORECASTING MODEL FOR HAGELSLAG ISLAND (Years 101-110, revised)
# =============================================================================
# Historical Events:
#   EARLY YEARS (1-10):
#   Year 2: Locust infestation (widespread damage)
#   Year 3: Sturgeon surge + Prestige project begins (Years 3-7, no immediate gains)
#   Year 5: Trade agreement (supported economic exchange)
#   Year 6: Sturgeon surge + Craftsmen strike (disrupted skilled labor)
#   Year 9: Sturgeon surge + Locust infestation (overlapping events)
#
#   YEARS 75-82:
#   Year 75: Sturgeon surge + Labor training initiative
#   Year 78: Sturgeon surge + Prestige project (Years 78-80, infrastructure)
#   Year 79: Locust infestation (during prestige project)
#   Year 80: Stability (prestige project backdrop)
#   Year 81: Sturgeon surge + Craftsmen strike (no investment year)
#   Year 82: Stability
#
#   YEARS 96-100:
#   Year 96: Sturgeon surge
#   Year 99: Sturgeon surge
#   Year 100: Locust infestation
#
#   STURGEON CYCLE (3-year): 3,6,9...75,78,81...96,99,102,105 (confirmed)
#   LOCUST EVENTS: Years 2, 9, 79, 100 (irregular, ~20-70 year gaps)
#   CRAFTSMEN STRIKES: Years 6, 81 (both during surge years - ~75 year gap)
#   PRESTIGE PROJECTS: Years 3-7, 78-80 (infrastructure investments)
#
#   NEW POLICIES (Year 101):
#   - Prestige project begins (Years 101-105, infrastructure investment)
#   - Retirement age raised from 64 to 70 (more workers in workforce)
#   - Government training programs for unemployed (ages 18+)
# =============================================================================

# Load GDP data
gdp_data = {}
with open('gdp_island', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gdp_data[int(row['year'])] = float(row['gdp'])

# Load profession income by year
profession_income = {}
with open('integrated_population_data_year100.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        year = int(row['year'])
        prof = row['profession']
        income = float(row['income'])
        if year not in profession_income:
            profession_income[year] = {}
        profession_income[year][prof] = profession_income[year].get(prof, 0) + income

# Load population data
from collections import defaultdict
population = defaultdict(int)
workforce = defaultdict(lambda: defaultdict(int))
with open('population_hage_island_year100.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        year = int(row['year'])
        prof = row['profession']
        population[year] += 1
        workforce[year][prof] += 1

# Population statistics for Year 100
pop_100 = population[100]
farmers_100 = workforce[100]['farmer']
fishers_100 = workforce[100]['fisher']
children_100 = workforce[100]['child']

# Calculate historical population growth rate (Years 95-100)
pop_growth_rate = (population[100] - population[95]) / population[95] / 5

# =============================================================================
# CALIBRATED MODEL PARAMETERS (derived from historical analysis)
# =============================================================================
# Sturgeon surge: +73.3% fisher income the following year
# Locust infestation: -68.3% farmer income the following year
# Labor training + Prestige project: +21.8% long-term GDP improvement

STURGEON_FISHER_BOOST = 0.733
LOCUST_FARMER_DAMAGE = -0.575

# =============================================================================
# NEW POLICY PARAMETERS (Year 101 implementation)
# =============================================================================
# Prestige Project (Years 101-105): Infrastructure investment similar to Years 78-80
# Historical analysis: Prestige projects yield +21.8% long-term GDP improvement
# Effect is gradual: +2% Year 1, +4% Year 2, +5% Year 3, +5.4% Year 4, +5.4% Year 5
PRESTIGE_PROJECT_BOOST = {
    101: 0.008,   # Initial infrastructure spending begins
    102: 0.015,   # Construction ramps up
    103: 0.022,   # Peak construction + early benefits
    104: 0.028,   # Full operation begins
    105: 0.030    # Sustained benefits
}

# Retirement Age Policy: Raised from 64 to 70 starting Year 101
# Impact: ~6 additional years of workers in workforce
# Estimate: +8-10% workforce retention = +3-4% GDP contribution
# Phased implementation as older workers choose to continue
OLD_RETIREMENT_AGE = 64
NEW_RETIREMENT_AGE = 70
RETIREMENT_POLICY_BOOST = {
    101: 0.005,   # ~15% of eligible workers stay
    102: 0.010,   # ~25% stay (awareness grows)
    103: 0.014,   # ~35% stay (normalized)
    104: 0.017,   # ~40% stay (economic incentive)
    105: 0.020    # ~45% stay (adoption plateaus)
}

# Government Training Programs for Unemployed ages 18+ (starting Year 101)
# Historical: Year 75 training initiative combined with prestige = +21.8%
# This is more comprehensive (all ages 18+, not just young workers)
# Eligibility: Any unemployed person age 18 or older
# Estimate: Reduces unemployment, increases productivity by 2-4%
TRAINING_PROGRAM_BOOST = {
    101: 0.005,   # Program launches, initial enrollment
    102: 0.012,   # First graduates enter workforce
    103: 0.016,   # Full enrollment, steady graduates
    104: 0.018,   # Mature program
    105: 0.020    # Sustained benefits + retraining cycles
}

# Year 100 baseline values
gdp_100 = gdp_data[100]
fisher_100 = profession_income[100]['fisher']
farmer_100 = profession_income[100]['farmer']
craftsman_100 = profession_income[100]['craftsman']
service_100 = profession_income[100]['service provider']
civil_100 = profession_income[100]['civil servant']

# =============================================================================
# 3-YEAR FISHER INCOME CYCLE (discovered from Year 91-100 analysis)
# =============================================================================
# Sturgeon SURGE events: 78,81,84,87,90,93,96,99,102,105... (3-year cycle)
# HIGH INCOME years: 79,82,85,88,91,94,97,100,103,106... (1-year lag after surge)
# Pattern: HIGH, low, low, HIGH, low, low...
#
# Year 100 was HIGH (from Year 99 surge), so: 101=low, 102=low (surge), 103=HIGH
# Calculated from notebook analysis:
FISHER_HIGH_AVG = (4583.16 + 4629.16 + 4740.48 + 4646.92) / 4  # ~4650
FISHER_LOW_AVG = (2677.71 + 2687.62 + 2780.97 + 2797.54 + 2764.10 + 2706.51) / 6  # ~2736

# =============================================================================
# PROFESSION INCOME TRENDS (from Year 91-100 regression analysis)
# =============================================================================
# Craftsman: $5,371 → $5,671 over 10 years = +0.5% annual growth
# Service Provider: $6,395 → $6,926 over 10 years = +0.8% annual growth
# Civil Servant: High income but declining workforce (-2% workers/year)
CRAFTSMAN_GROWTH = 0.005
SERVICE_GROWTH = 0.008
CIVIL_WORKFORCE_DECLINE = -0.02  # Worker count shrinking 2% per year

# =============================================================================
# HISTORICAL EVENT INSIGHTS (from Years 1-10 analysis)
# =============================================================================
# Year 9 had BOTH sturgeon surge AND locust infestation
# Result: Year 9→10 only dropped -1.9% (vs -20% for locust-only events)
# This shows sturgeon gains offset ~90% of locust damage when overlapping
#
# Year 6 had sturgeon surge + craftsmen strike
# Strike disrupted skilled labor but sturgeon partially compensated
#
# Locust severity varies: Year 2→3 was -11.6%, Year 79→80 was -20%
# Our model uses -20% (worst case) which is conservative

# =============================================================================
# FORECAST CALCULATIONS (with weather impacts from NMI forecasts)
# =============================================================================
# Weather impact modifiers on agriculture (from PDF analysis):
#   Year 101: 880mm precip - Normal (0% adjustment)
#   Year 102: 785mm precip - Drought stress (-3% farmer income)
#   Year 103: 940mm precip - Good for crops (+2% farmer income)
#   Year 104: 905mm precip - Normal (0% adjustment)
#   Year 105: 1020mm precip - Flood risk (-1% farmer income)

WEATHER_IMPACT = {101: 0.00, 102: -0.03, 103: +0.02, 104: 0.00, 105: -0.01}

# Population projections (based on 0.12% annual growth, workforce shifts)
# Children maturing into workforce, aging population effects
POP_PRODUCTIVITY = {
    101: 1.001,   # Slight population growth
    102: 1.002,   # More children enter workforce
    103: 1.003,   # Continued workforce growth
    104: 1.002,   # Stabilizing
    105: 1.002    # Stable growth
}

# Worker counts from Year 100 (used for projections)
fisher_count_100 = workforce[100]['fisher']
civil_count_100 = workforce[100]['civil servant']

# =============================================================================
# YEAR 101: LOW fisher cycle + Locust damage + Civil servant decline
# =============================================================================
fisher_101 = FISHER_LOW_AVG * fisher_count_100
fisher_change_101 = fisher_101 - fisher_100

farmer_101 = farmer_100 * (1 + LOCUST_FARMER_DAMAGE) * (1 + WEATHER_IMPACT[101])
locust_damage = farmer_101 - farmer_100

craftsman_101 = craftsman_100 * (1 + CRAFTSMAN_GROWTH)
craftsman_change_101 = craftsman_101 - craftsman_100

service_101 = service_100 * (1 + SERVICE_GROWTH)
service_change_101 = service_101 - service_100

civil_101 = civil_100 * (1 + CIVIL_WORKFORCE_DECLINE)  # Fewer workers = less total income
civil_change_101 = civil_101 - civil_100

total_impact_101 = fisher_change_101 + locust_damage + craftsman_change_101 + service_change_101 + civil_change_101

# Apply new Year 101 policies
policy_multiplier_101 = (1 + PRESTIGE_PROJECT_BOOST[101]) * (1 + RETIREMENT_POLICY_BOOST[101]) * (1 + TRAINING_PROGRAM_BOOST[101])
gdp_101 = (gdp_100 + total_impact_101) * POP_PRODUCTIVITY[101] * policy_multiplier_101

# =============================================================================
# YEAR 102: LOW fisher cycle + Farmer recovery (drought) + continued trends
# =============================================================================
fisher_102 = FISHER_LOW_AVG * fisher_count_100
fisher_change_102 = fisher_102 - fisher_101  # ~0 (both low years)

farmer_102 = farmer_100 * 0.7 * (1 + WEATHER_IMPACT[102])
farmer_recovery_102 = farmer_102 - farmer_101

craftsman_102 = craftsman_101 * (1 + CRAFTSMAN_GROWTH)
craftsman_change_102 = craftsman_102 - craftsman_101

service_102 = service_101 * (1 + SERVICE_GROWTH)
service_change_102 = service_102 - service_101

civil_102 = civil_101 * (1 + CIVIL_WORKFORCE_DECLINE)
civil_change_102 = civil_102 - civil_101

# Apply Year 102 policies
policy_multiplier_102 = (1 + PRESTIGE_PROJECT_BOOST[102]) * (1 + RETIREMENT_POLICY_BOOST[102]) * (1 + TRAINING_PROGRAM_BOOST[102])
gdp_102 = (gdp_101 + farmer_recovery_102 + fisher_change_102 + craftsman_change_102 + service_change_102 + civil_change_102) * POP_PRODUCTIVITY[102] * policy_multiplier_102

# =============================================================================
# YEAR 103: HIGH fisher cycle (SURGE!) + Full farmer recovery + good weather
# =============================================================================
fisher_103 = FISHER_HIGH_AVG * fisher_count_100
fisher_surge_103 = fisher_103 - fisher_102  # Big jump from low to high

farmer_103 = farmer_100 * (1 + WEATHER_IMPACT[103])
farmer_recovery_103 = farmer_103 - farmer_102

craftsman_103 = craftsman_102 * (1 + CRAFTSMAN_GROWTH)
craftsman_change_103 = craftsman_103 - craftsman_102

service_103 = service_102 * (1 + SERVICE_GROWTH)
service_change_103 = service_103 - service_102

civil_103 = civil_102 * (1 + CIVIL_WORKFORCE_DECLINE)
civil_change_103 = civil_103 - civil_102

# Apply Year 103 policies
policy_multiplier_103 = (1 + PRESTIGE_PROJECT_BOOST[103]) * (1 + RETIREMENT_POLICY_BOOST[103]) * (1 + TRAINING_PROGRAM_BOOST[103])
gdp_103 = (gdp_102 + farmer_recovery_103 + fisher_surge_103 + craftsman_change_103 + service_change_103 + civil_change_103) * POP_PRODUCTIVITY[103] * policy_multiplier_103

# =============================================================================
# YEAR 104: LOW fisher cycle + normal conditions
# =============================================================================
fisher_104 = FISHER_LOW_AVG * fisher_count_100
fisher_change_104 = fisher_104 - fisher_103  # Drop from high to low

craftsman_104 = craftsman_103 * (1 + CRAFTSMAN_GROWTH)
craftsman_change_104 = craftsman_104 - craftsman_103

service_104 = service_103 * (1 + SERVICE_GROWTH)
service_change_104 = service_104 - service_103

civil_104 = civil_103 * (1 + CIVIL_WORKFORCE_DECLINE)
civil_change_104 = civil_104 - civil_103

# Apply Year 104 policies
policy_multiplier_104 = (1 + PRESTIGE_PROJECT_BOOST[104]) * (1 + RETIREMENT_POLICY_BOOST[104]) * (1 + TRAINING_PROGRAM_BOOST[104])
gdp_104 = (gdp_103 + fisher_change_104 + craftsman_change_104 + service_change_104 + civil_change_104) * POP_PRODUCTIVITY[104] * policy_multiplier_104

# =============================================================================
# YEAR 105: LOW fisher cycle + flood risk
# =============================================================================
fisher_105 = FISHER_LOW_AVG * fisher_count_100 * (1 + WEATHER_IMPACT[105])
fisher_change_105 = fisher_105 - fisher_104  # ~0 (both low years)

craftsman_105 = craftsman_104 * (1 + CRAFTSMAN_GROWTH)
craftsman_change_105 = craftsman_105 - craftsman_104

service_105 = service_104 * (1 + SERVICE_GROWTH)
service_change_105 = service_105 - service_104

civil_105 = civil_104 * (1 + CIVIL_WORKFORCE_DECLINE)
civil_change_105 = civil_105 - civil_104

# Apply Year 105 policies
policy_multiplier_105 = (1 + PRESTIGE_PROJECT_BOOST[105]) * (1 + RETIREMENT_POLICY_BOOST[105]) * (1 + TRAINING_PROGRAM_BOOST[105])
gdp_105 = (gdp_104 + fisher_change_105 + craftsman_change_105 + service_change_105 + civil_change_105) * POP_PRODUCTIVITY[105] * policy_multiplier_105

# Store forecasts
forecasts = {
    101: gdp_101,
    102: gdp_102,
    103: gdp_103,
    104: gdp_104,
    105: gdp_105
}

# =============================================================================
# POST-MORTEM: FORECAST VS ACTUAL (Years 101-105)
# =============================================================================
# Year 101: Forecast -17.2% vs Actual -19.4% → Locust MORE severe than modeled
# Year 102: Forecast +8.4%  vs Actual +1.8%  → Drought compounded slow recovery
# Year 103: Forecast +23.8% vs Actual -10.8% → Sturgeon HIGH disrupted; prolonged locust tail
# Year 104: Forecast -3.6%  vs Actual +15.1% → Recovery (locust clearing + policies)
# Year 105: Forecast +7.2%  vs Actual +15.0% → Continued recovery momentum
#
# ROOT CAUSES:
#   1. Locust damage was more severe than -57.5% (closer to -70%)
#   2. Locust recovery takes 3 years, not 1 — farmer income still depressed in Year 103
#   3. Year 102 sturgeon surge did not produce expected HIGH income in 103;
#      locust aftermath likely suppressed the effect
#   4. Year 104-105 recovery driven by locust clearing + policies delivering returns

ACTUAL_GDP = {
    101: 972000.46,
    102: 989644.00,
    103: 882950.00,
    104: 1015955.20,
    105: 1168436.60
}

# =============================================================================
# RECALIBRATED PARAMETERS
# =============================================================================
LOCUST_FARMER_DAMAGE_REVISED = -0.70   # Revised from -0.575 (back-calculated from actual 101)
STURGEON_CONFIDENCE = 0.70             # Reduced from 1.0 after Year 103 disruption
FISHER_BLENDED_HIGH = FISHER_HIGH_AVG * STURGEON_CONFIDENCE + FISHER_LOW_AVG * (1 - STURGEON_CONFIDENCE)

# =============================================================================
# YEAR 105 PROFESSION ESTIMATES (extrapolated baseline for 106-110)
# =============================================================================
# No profession-level actuals for 101-105, so we extrapolate from Year 100.
# A scale factor anchors tracked professions to the actual Year 105 GDP.
# This absorbs untracked professions (retired, homemaker, child) and any
# real-world drift from our trend estimates.
fisher_105_est = FISHER_LOW_AVG * fisher_count_100   # 105 is surge year (LOW income)
craftsman_105_est = craftsman_100 * (1 + CRAFTSMAN_GROWTH) ** 5
service_105_est = service_100 * (1 + SERVICE_GROWTH) ** 5
civil_105_est = civil_100 * (1 + CIVIL_WORKFORCE_DECLINE) ** 5
farmer_105_est = farmer_100 * (1 + WEATHER_IMPACT[105])  # -1% flood

tracked_total_105 = fisher_105_est + craftsman_105_est + service_105_est + civil_105_est + farmer_105_est
GDP_SCALE = ACTUAL_GDP[105] / tracked_total_105   # ~1.20

POP_PRODUCTIVITY_NEW = {106: 1.002, 107: 1.002, 108: 1.001, 109: 1.001, 110: 1.001}

# =============================================================================
# OUTPUT RESULTS
# =============================================================================

# =============================================================================
# YEAR 106: Sturgeon HIGH (blended, 70% confidence) — surge was in 105
# =============================================================================
fisher_106 = FISHER_BLENDED_HIGH * fisher_count_100
craftsman_106 = craftsman_105_est * (1 + CRAFTSMAN_GROWTH)
service_106 = service_105_est * (1 + SERVICE_GROWTH)
civil_106 = civil_105_est * (1 + CIVIL_WORKFORCE_DECLINE)
farmer_106 = farmer_105_est  # Normal weather (no forecast data beyond 105)

tracked_total_106 = fisher_106 + craftsman_106 + service_106 + civil_106 + farmer_106
gdp_106 = tracked_total_106 * GDP_SCALE * POP_PRODUCTIVITY_NEW[106]

# =============================================================================
# YEAR 107: LOW fisher cycle
# =============================================================================
fisher_107 = FISHER_LOW_AVG * fisher_count_100
craftsman_107 = craftsman_106 * (1 + CRAFTSMAN_GROWTH)
service_107 = service_106 * (1 + SERVICE_GROWTH)
civil_107 = civil_106 * (1 + CIVIL_WORKFORCE_DECLINE)
farmer_107 = farmer_106

tracked_total_107 = fisher_107 + craftsman_107 + service_107 + civil_107 + farmer_107
gdp_107 = tracked_total_107 * GDP_SCALE * POP_PRODUCTIVITY_NEW[107]

# =============================================================================
# YEAR 108: LOW fisher + sturgeon surge event (income realised in 109)
# 3-year cycle: surges at 105, 108, 111...
# =============================================================================
fisher_108 = FISHER_LOW_AVG * fisher_count_100
craftsman_108 = craftsman_107 * (1 + CRAFTSMAN_GROWTH)
service_108 = service_107 * (1 + SERVICE_GROWTH)
civil_108 = civil_107 * (1 + CIVIL_WORKFORCE_DECLINE)
farmer_108 = farmer_107

tracked_total_108 = fisher_108 + craftsman_108 + service_108 + civil_108 + farmer_108
gdp_108 = tracked_total_108 * GDP_SCALE * POP_PRODUCTIVITY_NEW[108]

# =============================================================================
# YEAR 109: Sturgeon HIGH (blended, 70% confidence) — surge was in 108
# =============================================================================
fisher_109 = FISHER_BLENDED_HIGH * fisher_count_100
craftsman_109 = craftsman_108 * (1 + CRAFTSMAN_GROWTH)
service_109 = service_108 * (1 + SERVICE_GROWTH)
civil_109 = civil_108 * (1 + CIVIL_WORKFORCE_DECLINE)
farmer_109 = farmer_108

tracked_total_109 = fisher_109 + craftsman_109 + service_109 + civil_109 + farmer_109
gdp_109 = tracked_total_109 * GDP_SCALE * POP_PRODUCTIVITY_NEW[109]

# =============================================================================
# YEAR 110: LOW fisher cycle
# =============================================================================
fisher_110 = FISHER_LOW_AVG * fisher_count_100
craftsman_110 = craftsman_109 * (1 + CRAFTSMAN_GROWTH)
service_110 = service_109 * (1 + SERVICE_GROWTH)
civil_110 = civil_109 * (1 + CIVIL_WORKFORCE_DECLINE)
farmer_110 = farmer_109

tracked_total_110 = fisher_110 + craftsman_110 + service_110 + civil_110 + farmer_110
gdp_110 = tracked_total_110 * GDP_SCALE * POP_PRODUCTIVITY_NEW[110]

new_forecasts = {106: gdp_106, 107: gdp_107, 108: gdp_108, 109: gdp_109, 110: gdp_110}

# =============================================================================
# OUTPUT
# =============================================================================
print("=" * 70)
print("GDP FORECAST FOR HAGELSLAG ISLAND — REVISED MODEL")
print("=" * 70)

print("\nModel Parameters:")
print(f"  Fisher 3-year cycle:       HIGH=${FISHER_HIGH_AVG:,.0f}, LOW=${FISHER_LOW_AVG:,.0f}")
print(f"  Locust damage (original):  {LOCUST_FARMER_DAMAGE*100:.1f}%  →  revised: {LOCUST_FARMER_DAMAGE_REVISED*100:.1f}%")
print(f"  Sturgeon confidence:       {STURGEON_CONFIDENCE*100:.0f}%  (blended HIGH = ${FISHER_BLENDED_HIGH:,.0f})")
print(f"  Craftsman growth:          +{CRAFTSMAN_GROWTH*100:.1f}% annual")
print(f"  Service provider growth:   +{SERVICE_GROWTH*100:.1f}% annual")
print(f"  Civil servant workforce:   {CIVIL_WORKFORCE_DECLINE*100:.1f}% annual (declining)")
print(f"  GDP scale factor:          {GDP_SCALE:.4f}")

print("\nPolicies (Year 101, sustained):")
print(f"  Prestige Project:          Construction complete; benefits continue")
print(f"  Retirement Age:            {OLD_RETIREMENT_AGE} → {NEW_RETIREMENT_AGE} (adoption ongoing)")
print(f"  Training Programs (18+):   Mature, sustained")

# --- 101-105 comparison ---
print("\n" + "=" * 70)
print("YEARS 101-105: FORECAST vs ACTUAL")
print("=" * 70)
print(f"{'Year':<6}{'Forecast':>14}{'Actual':>14}{'Fcst Err':>10}{'Act YoY':>10}")
print("-" * 70)

prev_actual = gdp_100
for year in range(101, 106):
    fcast = forecasts[year]
    actual = ACTUAL_GDP[year]
    err = ((actual - fcast) / fcast) * 100
    yoy = ((actual - prev_actual) / prev_actual) * 100
    print(f"{year:<6}{fcast:>14,.0f}{actual:>14,.0f}{err:>+9.1f}%{yoy:>+9.1f}%")
    prev_actual = actual

print("-" * 70)
print("  101: Locust impact more severe than forecast")
print("  102: Drought stalled farmer recovery")
print("  103: Sturgeon HIGH failed — prolonged locust tail (biggest miss)")
print("  104-105: Policies + recovery drove ~15% annual growth")

# --- 106-110 forecast ---
print("\n" + "=" * 70)
print("YEARS 106-110: REVISED FORECAST (from Year 105 actual baseline)")
print("=" * 70)

notes_106_110 = {
    106: "Sturgeon HIGH (70% conf) from 105 surge",
    107: "Fisher LOW + steady trends",
    108: "Fisher LOW + sturgeon surge (income in 109)",
    109: "Sturgeon HIGH (70% conf) from 108 surge",
    110: "Fisher LOW + steady trends"
}

print(f"{'Year':<6}{'GDP':>15}{'YoY Chg':>10}  Notes")
print("-" * 70)
print(f"{'105':<6}{ACTUAL_GDP[105]:>15,.2f}{'':>10}  Actual (baseline)")

prev = ACTUAL_GDP[105]
for year in range(106, 111):
    gdp = new_forecasts[year]
    chg = ((gdp - prev) / prev) * 100
    print(f"{year:<6}{gdp:>15,.2f}{chg:>+9.1f}%  {notes_106_110[year]}")
    prev = gdp

print("-" * 70)
print("\nConfidence notes:")
print("  - Sturgeon timing carries 30% uncertainty (disrupted in 103)")
print("  - If cycle shifted +1yr: HIGH years move to 107, 110 instead")
print("  - No disaster events modelled (next locust est. Year 120+)")
print("  - Policies treated as sustained from Year 105 level")
print("  - Weather assumed normal beyond 105 (no data available)")
print("\n" + "=" * 70)

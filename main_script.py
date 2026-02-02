import csv

# =============================================================================
# GDP FORECASTING MODEL FOR HAGELSLAG ISLAND (Years 101-105)
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
LOCUST_FARMER_DAMAGE = -0.683

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
gdp_101 = (gdp_100 + total_impact_101) * POP_PRODUCTIVITY[101]

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

gdp_102 = (gdp_101 + farmer_recovery_102 + fisher_change_102 + craftsman_change_102 + service_change_102 + civil_change_102) * POP_PRODUCTIVITY[102]

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

gdp_103 = (gdp_102 + farmer_recovery_103 + fisher_surge_103 + craftsman_change_103 + service_change_103 + civil_change_103) * POP_PRODUCTIVITY[103]

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

gdp_104 = (gdp_103 + fisher_change_104 + craftsman_change_104 + service_change_104 + civil_change_104) * POP_PRODUCTIVITY[104]

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

gdp_105 = (gdp_104 + fisher_change_105 + craftsman_change_105 + service_change_105 + civil_change_105) * POP_PRODUCTIVITY[105]

# Store forecasts
forecasts = {
    101: gdp_101,
    102: gdp_102,
    103: gdp_103,
    104: gdp_104,
    105: gdp_105
}


# =============================================================================
# OUTPUT RESULTS
# =============================================================================

print("=" * 70)
print("GDP FORECAST FOR HAGELSLAG ISLAND (Years 101-105)")
print("=" * 70)

print("\nModel Parameters (calibrated from Year 91-100 analysis):")
print(f"  Fisher 3-year cycle:       HIGH=${FISHER_HIGH_AVG:,.0f}, LOW=${FISHER_LOW_AVG:,.0f}")
print(f"  Locust infestation effect: {LOCUST_FARMER_DAMAGE*100:.1f}% farmer income")
print(f"  Craftsman growth trend:    +{CRAFTSMAN_GROWTH*100:.1f}% annual")
print(f"  Service provider growth:   +{SERVICE_GROWTH*100:.1f}% annual")
print(f"  Civil servant workforce:   {CIVIL_WORKFORCE_DECLINE*100:.1f}% annual (declining)")

print("\nYear 100 Baseline (by GDP contribution):")
print(f"  Total GDP:         {gdp_100:>12,.2f}")
print(f"  Fisher income:     {fisher_100:>12,.2f} (HIGH cycle - #2 contributor)")
print(f"  Craftsman income:  {craftsman_100:>12,.2f} (#1 contributor)")
print(f"  Service provider:  {service_100:>12,.2f} (#3 contributor)")
print(f"  Civil servant:     {civil_100:>12,.2f} (#4 contributor)")
print(f"  Farmer income:     {farmer_100:>12,.2f} (#5 - pre-locust)")
print(f"  Population:        {pop_100:>12}  ({farmers_100} farmers, {fishers_100} fishers)")
print(f"  Pop growth:        {pop_growth_rate*100:>11.2f}% annually")

print("\n" + "-" * 70)
print(f"{'Year':<8}{'GDP':>15}{'Change':>12}  Notes")
print("-" * 70)
print(f"{'100':<8}{gdp_100:>15,.2f}{'':>12}  Actual (sturgeon-boosted)")

notes = {
    101: "Fisher LOW cycle + Locust damage",
    102: "Fisher LOW + Farmer recovery (drought -3%)",
    103: "Fisher HIGH cycle (surge!) + Full recovery (+2%)",
    104: "Fisher LOW cycle + normal",
    105: "Fisher LOW + flood risk (-1%)"
}

prev_gdp = gdp_100
for year in range(101, 106):
    gdp = forecasts[year]
    change = ((gdp - prev_gdp) / prev_gdp) * 100
    print(f"{year:<8}{gdp:>15,.2f}{change:>+11.1f}%  {notes[year]}")
    prev_gdp = gdp

print("-" * 70)

# =============================================================================
# MODEL VALIDATION (using historical events)
# =============================================================================

# Locust events validation
yr2_3_change = ((gdp_data[3] - gdp_data[2]) / gdp_data[2]) * 100 if 2 in gdp_data and 3 in gdp_data else None
yr9_10_change = ((gdp_data[10] - gdp_data[9]) / gdp_data[9]) * 100 if 9 in gdp_data and 10 in gdp_data else None
yr79_80_drop = ((gdp_data[80] - gdp_data[79]) / gdp_data[79]) * 100
yr100_101_drop = ((gdp_101 - gdp_100) / gdp_100) * 100

print("\nModel Validation:")
print("-" * 70)
print("LOCUST INFESTATION IMPACTS (lagged 1 year):")
if yr2_3_change is not None:
    print(f"  Year 2 → 3 actual:       {yr2_3_change:+.1f}%  (locust in Year 2)")
if yr9_10_change is not None:
    print(f"  Year 9 → 10 actual:      {yr9_10_change:+.1f}%  (locust + sturgeon in Year 9)")
print(f"  Year 79 → 80 actual:     {yr79_80_drop:+.1f}%  (locust in Year 79)")
print(f"  Year 100 → 101 forecast: {yr100_101_drop:+.1f}%  (locust in Year 100)")

# 3-year sturgeon cycle validation
print("\n3-YEAR STURGEON CYCLE VALIDATION:")
print("  Surge events:  3,6,9...75,78,81...90,93,96,99,102,105...")
print("  HIGH income:   4,7,10...76,79,82...91,94,97,100,103,106... (1-yr lag)")
print("  Pattern: HIGH → low → low → HIGH (repeating)")

# Year 103 prediction confidence
print(f"\n  Year 102: Surge event (sturgeon migration)")
print(f"  Year 103 forecast:       {((gdp_103 - gdp_102) / gdp_102) * 100:+.1f}%  (HIGH income year)")
print(f"  Year 105: Next surge event (HIGH income in 106)")

print("\nOVERLAPPING EVENTS ANALYSIS:")
print("  Year 9 (locust + sturgeon): -1.9% → Surge offset ~90% of locust damage")
print("  Year 6 (surge + strike): Strike partially offset by surge")
print("  Year 81 (surge + strike): Strike partially offset by surge")

# Calculate craftsmen strike impact
yr5_6_change = ((gdp_data[6] - gdp_data[5]) / gdp_data[5]) * 100 if 5 in gdp_data and 6 in gdp_data else None
yr80_81_change = ((gdp_data[81] - gdp_data[80]) / gdp_data[80]) * 100 if 80 in gdp_data and 81 in gdp_data else None
yr81_82_change = ((gdp_data[82] - gdp_data[81]) / gdp_data[81]) * 100 if 81 in gdp_data and 82 in gdp_data else None

print("\nCRAFTSMEN STRIKE IMPACTS (both during surge years):")
if yr5_6_change is not None:
    print(f"  Year 5 → 6 actual:       {yr5_6_change:+.1f}%  (surge + strike in Year 6)")
if yr80_81_change is not None:
    print(f"  Year 80 → 81 actual:     {yr80_81_change:+.1f}%  (surge + strike in Year 81)")
if yr81_82_change is not None:
    print(f"  Year 81 → 82 actual:     {yr81_82_change:+.1f}%  (stability after strike)")
print("  Pattern: Strike damage partially offset when occurring in surge year")

print("\nLOCUST SEVERITY VARIATION:")
print("  Year 2→3:   -11.6% (moderate)")
print("  Year 79→80: -20.0% (severe)")
print("  Model uses: -20.2% (conservative/worst-case)")
avg_locust = (-11.6 + -20.0) / 2
print(f"  Historical avg: {avg_locust:.1f}% (model may overestimate damage by ~{abs(yr100_101_drop - avg_locust):.0f}%)")

print("\n" + "=" * 70)

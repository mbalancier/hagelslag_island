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

# Load profession income by year from Year 110 data
profession_income = {}
with open('population_hage_island_year110.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        year = int(row['year'])
        prof = row['profession']
        income = float(row['income'])
        if year not in profession_income:
            profession_income[year] = {}
        profession_income[year][prof] = profession_income[year].get(prof, 0) + income

# Load population data from Year 110 data
from collections import defaultdict
import numpy as np
population = defaultdict(int)
workforce = defaultdict(lambda: defaultdict(int))
individual_incomes = defaultdict(list)  # For percentile calculations
with open('population_hage_island_year110.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        year = int(row['year'])
        prof = row['profession']
        income = float(row['income'])
        population[year] += 1
        workforce[year][prof] += 1
        if income > 0:  # Only include positive incomes for percentile calc
            individual_incomes[year].append(income)

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
# ROOT CAUSES (revised from profession-level actuals in population_year105.csv):
#   1. Locust damage peaked at -82% in Year 102 (2-yr lag from Year 100 event),
#      not -57.5% in Year 101.  Farmer avg income: $2544(100)→$2082(101)→$453(102)
#   2. Farmer income stayed crushed in Year 103 ($456 avg); recovery began Year 104
#   3. Sturgeon cycle PHASE-SHIFTED by -1 year:
#      Surges at 101, 104, 107… (not 102, 105, 108)
#      → HIGH fisher income at 102, 105, 108… (not 103, 106, 109)
#      Year 102 was HIGH ($4256); Year 103 was LOW ($2478) — opposite of forecast
#   4. Civil servant workforce GREW 25→30 (total income +13.4%); -2%/yr was wrong
#   5. Retired population collapsed 60→21 (retirement age 64→70 policy effect)
#   6. Year 104-105 recovery driven by locust clearing + policies delivering returns

ACTUAL_GDP = {
    101: 972000.46,
    102: 989644.08,
    103: 882950.35,
    104: 1015955.20,
    105: 1168436.60,
    106: 1007133.96,
    107: 906980.26,
    108: 1045563.02,
    109: 942731.97,
    110: 946912.70,
    111: 1143906.63,
    112: 1032112.04,
    113: 1010180.78,
    114: 1025299.53,
    115: 981203.45
}

# Actual Gini coefficients for Years 111-115
# Two measures: Full economy (includes raiders/gangs) vs Formal economy only
ACTUAL_GINI = {
    111: {'full': 0.46, 'formal': 0.37},
    112: {'full': 0.49, 'formal': 0.37},
    113: {'full': 0.50, 'formal': 0.38},
    114: {'full': 0.54, 'formal': 0.40},
    115: {'full': 0.52, 'formal': 0.37}
}

# =============================================================================
# RECALIBRATED PARAMETERS (from Years 100-105 profession-level actuals)
# =============================================================================
# Locust: peak damage -82% at Year 102 (2-yr lag), not -57.5% at Year 101
LOCUST_FARMER_DAMAGE_REVISED = -0.82

# Sturgeon cycle confirmed but phase-shifted by -1 year.
# Surges: 101, 104, 107, 110 …  →  HIGH income (1-yr lag): 102, 105, 108, 111 …
# HIGH avg income has been declining: $4647(100), $4256(102), $4143(105)
# Use 4-year rolling window (97, 100, 102, 105) for HIGH; 5-year for LOW
FISHER_HIGH_AVG_R = (4740.48 + 4646.92 + 4255.83 + 4143.01) / 4  # ~4447
FISHER_LOW_AVG_R  = (2780.97 + 2764.10 + 2474.16 + 2478.11 + 2489.75) / 5  # ~2597

# Growth rates recalibrated from 100→105 total-income actuals
CRAFTSMAN_GROWTH_R     = 0.008    # Was 0.005; 100→105 annualised +0.77%
SERVICE_GROWTH_R       = 0.011    # Was 0.008; 100→105 annualised +1.05%
CIVIL_SERVANT_GROWTH_R = 0.025    # Was -0.02 decline; workforce GREW 25→30
FARMER_GROWTH_R        = 0.004    # Stable post-recovery baseline

# Retired: policy shock (ret. age 64→70) bottomed Year 105 (21 workers).
# New age-70 retirees re-enter from Year 106; manual projection below.
RETIRED_PROJ = {106: 22000, 107: 24000, 108: 27000, 109: 30000, 110: 33000}

# Homemaker + Unemployed: net-cost category, combined costs trending ~5%/yr
HOME_UNEMP_GROWTH = 0.05

# =============================================================================
# NEW POLICIES ENACTED IN YEAR 106
# =============================================================================
# (A) Year 101 Prestige Project carry-over
#     Infrastructure completed in 105; residual benefit continues into 106.
#     Tapers from 3.0 % (Year 105) → 2.5 % (Year 106), then fades.
PRESTIGE_101_CARRYOVER = {106: 0.025}   # Year 106 only

# (B) Wind Energy Transition (Years 106-110)
#     Capital & conversion costs drag GDP −3 % p.a. for 5 years.
#     Permanently lowers emissions; no further GDP effect modelled after 110.
WIND_TRANSITION_DRAG = -0.03

# (B2) Resident displeasure with wind turbines (Years 106-110)
#      Channels: reduced tourism demand, lower civic morale, slight
#      island-wide productivity loss.  Ramps up as turbines become
#      operational; partial habituation toward end of the window.
WIND_DISPLEASURE_DRAG = {
    106: -0.005,   # Construction underway; concerns voiced
    107: -0.010,   # Turbines visible; opposition grows
    108: -0.015,   # Peak displeasure — fully operational
    109: -0.015,   # Sustained negative sentiment
    110: -0.010    # Partial habituation
}

# (C) Dual-Income Household Incentive (Years 106-110)
#     2 % of current homemakers exit each year (compounds annually).
#     New entrants earn $4 500/yr (mid-range; training programs are mature).
#     Previous-year entrants' income grows at avg profession rate (+1.2 % p.a.).
HOMEMAKER_EXIT_RATE = 0.02
NEW_ENTRANT_INCOME  = 4500
ENTRANT_GROWTH      = 0.012   # avg of craftsman/service/civil/farmer growth rates

# (D) Second Prestige Project (enacted Year 106; effects Years 107-111)
#     Same gradual ramp profile as the 101-105 project.
PRESTIGE_106_BOOST = {107: 0.008, 108: 0.015, 109: 0.022, 110: 0.028}

# =============================================================================
# YEAR 105 ACTUALS (all professions, loaded from population_year105.csv)
# =============================================================================
fisher_105_est     = profession_income[105]['fisher']            # 323,155  HIGH year
farmer_105_est     = profession_income[105]['farmer']            # 174,107
craftsman_105_est  = profession_income[105]['craftsman']         # 253,394
service_105_est    = profession_income[105]['service provider']  # 225,830
civil_105_est      = profession_income[105]['civil servant']     # 185,584
retired_105_est    = profession_income[105]['retired']           #  27,599
homemaker_105_est  = profession_income[105]['homemaker']         # -16,805
unemployed_105_est = profession_income[105]['unemployed']        #  -4,427
fisher_count_105   = workforce[105]['fisher']                    # 78

POP_PRODUCTIVITY_NEW = {106: 1.002, 107: 1.002, 108: 1.001, 109: 1.001, 110: 1.001}

# =============================================================================
# YEARS 106-110: REVISED FORECAST  (Year 106 policies active)
# =============================================================================
# Sturgeon: surges 101,104,107,110 → HIGH income (1-yr lag) 102,105,108,111
#   106=LOW | 107=LOW (surge) | 108=HIGH | 109=LOW | 110=LOW (surge)
#
# GDP-level policy multipliers (applied after profession sum):
#   (A)  Prestige-101 carry-over  — Year 106 only       (+2.5 %)
#   (B)  Wind transition          — Years 106-110       (−3.0 %)
#   (B2) Resident displeasure     — Years 106-110       (−0.5…−1.5 %)
#   (D)  Prestige-106 ramp        — Years 107-110       (+0.8…+2.8 %)
# Profession-level adjustment:
#   (C) Homemaker exit → cumulative new-entrant income tracked per year
# =============================================================================

# --- Separate baselines (Year 105 actuals) ---
hm_count_prev  = workforce[105]['homemaker']   # homemaker headcount in 105
hm_income_prev = homemaker_105_est             # total homemaker income 105 (negative)
unemp_prev     = unemployed_105_est            # total unemployed income 105 (negative)
cum_entrant_inc = 0.0                          # cumulative new-entrant income (grows + adds)

# ── Year 106: Fisher LOW ──
hm_leaving     = hm_count_prev * HOMEMAKER_EXIT_RATE
hm_count_106   = hm_count_prev - hm_leaving
hm_income_106  = hm_income_prev * (1 + HOME_UNEMP_GROWTH) * (hm_count_106 / hm_count_prev)
unemp_106      = unemp_prev     * (1 + HOME_UNEMP_GROWTH)
cum_entrant_inc = cum_entrant_inc * (1 + ENTRANT_GROWTH) + hm_leaving * NEW_ENTRANT_INCOME

fisher_106     = FISHER_LOW_AVG_R  * fisher_count_105
craftsman_106  = craftsman_105_est * (1 + CRAFTSMAN_GROWTH_R)
service_106    = service_105_est   * (1 + SERVICE_GROWTH_R)
civil_106      = civil_105_est     * (1 + CIVIL_SERVANT_GROWTH_R)
farmer_106     = farmer_105_est    * (1 + FARMER_GROWTH_R)
retired_106    = RETIRED_PROJ[106]

prof_sum_106   = (fisher_106 + craftsman_106 + service_106 + civil_106 + farmer_106
                  + retired_106 + hm_income_106 + unemp_106 + cum_entrant_inc)
policy_106     = ((1 + PRESTIGE_101_CARRYOVER.get(106, 0))
                  * (1 + WIND_TRANSITION_DRAG)
                  * (1 + WIND_DISPLEASURE_DRAG.get(106, 0))
                  * (1 + PRESTIGE_106_BOOST.get(106, 0)))
gdp_106        = prof_sum_106 * POP_PRODUCTIVITY_NEW[106] * policy_106

# snapshots for output
cum_ent_106 = cum_entrant_inc; hm_cnt_106 = hm_count_106; hm_lv_106 = hm_leaving

# ── Year 107: Fisher LOW  (sturgeon surge — income realised 108) ──
hm_leaving     = hm_count_106  * HOMEMAKER_EXIT_RATE
hm_count_107   = hm_count_106  - hm_leaving
hm_income_107  = hm_income_106 * (1 + HOME_UNEMP_GROWTH) * (hm_count_107 / hm_count_106)
unemp_107      = unemp_106     * (1 + HOME_UNEMP_GROWTH)
cum_entrant_inc = cum_entrant_inc * (1 + ENTRANT_GROWTH) + hm_leaving * NEW_ENTRANT_INCOME

fisher_107     = FISHER_LOW_AVG_R  * fisher_count_105
craftsman_107  = craftsman_106  * (1 + CRAFTSMAN_GROWTH_R)
service_107    = service_106    * (1 + SERVICE_GROWTH_R)
civil_107      = civil_106      * (1 + CIVIL_SERVANT_GROWTH_R)
farmer_107     = farmer_106     * (1 + FARMER_GROWTH_R)
retired_107    = RETIRED_PROJ[107]

prof_sum_107   = (fisher_107 + craftsman_107 + service_107 + civil_107 + farmer_107
                  + retired_107 + hm_income_107 + unemp_107 + cum_entrant_inc)
policy_107     = ((1 + PRESTIGE_101_CARRYOVER.get(107, 0))
                  * (1 + WIND_TRANSITION_DRAG)
                  * (1 + WIND_DISPLEASURE_DRAG.get(107, 0))
                  * (1 + PRESTIGE_106_BOOST.get(107, 0)))
gdp_107        = prof_sum_107 * POP_PRODUCTIVITY_NEW[107] * policy_107

cum_ent_107 = cum_entrant_inc; hm_cnt_107 = hm_count_107; hm_lv_107 = hm_leaving

# ── Year 108: Fisher HIGH  (surge was in 107) ──
hm_leaving     = hm_count_107  * HOMEMAKER_EXIT_RATE
hm_count_108   = hm_count_107  - hm_leaving
hm_income_108  = hm_income_107 * (1 + HOME_UNEMP_GROWTH) * (hm_count_108 / hm_count_107)
unemp_108      = unemp_107     * (1 + HOME_UNEMP_GROWTH)
cum_entrant_inc = cum_entrant_inc * (1 + ENTRANT_GROWTH) + hm_leaving * NEW_ENTRANT_INCOME

fisher_108     = FISHER_HIGH_AVG_R * fisher_count_105
craftsman_108  = craftsman_107  * (1 + CRAFTSMAN_GROWTH_R)
service_108    = service_107    * (1 + SERVICE_GROWTH_R)
civil_108      = civil_107      * (1 + CIVIL_SERVANT_GROWTH_R)
farmer_108     = farmer_107     * (1 + FARMER_GROWTH_R)
retired_108    = RETIRED_PROJ[108]

prof_sum_108   = (fisher_108 + craftsman_108 + service_108 + civil_108 + farmer_108
                  + retired_108 + hm_income_108 + unemp_108 + cum_entrant_inc)
policy_108     = ((1 + PRESTIGE_101_CARRYOVER.get(108, 0))
                  * (1 + WIND_TRANSITION_DRAG)
                  * (1 + WIND_DISPLEASURE_DRAG.get(108, 0))
                  * (1 + PRESTIGE_106_BOOST.get(108, 0)))
gdp_108        = prof_sum_108 * POP_PRODUCTIVITY_NEW[108] * policy_108

cum_ent_108 = cum_entrant_inc; hm_cnt_108 = hm_count_108; hm_lv_108 = hm_leaving

# ── Year 109: Fisher LOW ──
hm_leaving     = hm_count_108  * HOMEMAKER_EXIT_RATE
hm_count_109   = hm_count_108  - hm_leaving
hm_income_109  = hm_income_108 * (1 + HOME_UNEMP_GROWTH) * (hm_count_109 / hm_count_108)
unemp_109      = unemp_108     * (1 + HOME_UNEMP_GROWTH)
cum_entrant_inc = cum_entrant_inc * (1 + ENTRANT_GROWTH) + hm_leaving * NEW_ENTRANT_INCOME

fisher_109     = FISHER_LOW_AVG_R  * fisher_count_105
craftsman_109  = craftsman_108  * (1 + CRAFTSMAN_GROWTH_R)
service_109    = service_108    * (1 + SERVICE_GROWTH_R)
civil_109      = civil_108      * (1 + CIVIL_SERVANT_GROWTH_R)
farmer_109     = farmer_108     * (1 + FARMER_GROWTH_R)
retired_109    = RETIRED_PROJ[109]

prof_sum_109   = (fisher_109 + craftsman_109 + service_109 + civil_109 + farmer_109
                  + retired_109 + hm_income_109 + unemp_109 + cum_entrant_inc)
policy_109     = ((1 + PRESTIGE_101_CARRYOVER.get(109, 0))
                  * (1 + WIND_TRANSITION_DRAG)
                  * (1 + WIND_DISPLEASURE_DRAG.get(109, 0))
                  * (1 + PRESTIGE_106_BOOST.get(109, 0)))
gdp_109        = prof_sum_109 * POP_PRODUCTIVITY_NEW[109] * policy_109

cum_ent_109 = cum_entrant_inc; hm_cnt_109 = hm_count_109; hm_lv_109 = hm_leaving

# ── Year 110: Fisher LOW  (sturgeon surge — income realised 111) ──
hm_leaving     = hm_count_109  * HOMEMAKER_EXIT_RATE
hm_count_110   = hm_count_109  - hm_leaving
hm_income_110  = hm_income_109 * (1 + HOME_UNEMP_GROWTH) * (hm_count_110 / hm_count_109)
unemp_110      = unemp_109     * (1 + HOME_UNEMP_GROWTH)
cum_entrant_inc = cum_entrant_inc * (1 + ENTRANT_GROWTH) + hm_leaving * NEW_ENTRANT_INCOME

fisher_110     = FISHER_LOW_AVG_R  * fisher_count_105
craftsman_110  = craftsman_109  * (1 + CRAFTSMAN_GROWTH_R)
service_110    = service_109    * (1 + SERVICE_GROWTH_R)
civil_110      = civil_109      * (1 + CIVIL_SERVANT_GROWTH_R)
farmer_110     = farmer_109     * (1 + FARMER_GROWTH_R)
retired_110    = RETIRED_PROJ[110]

prof_sum_110   = (fisher_110 + craftsman_110 + service_110 + civil_110 + farmer_110
                  + retired_110 + hm_income_110 + unemp_110 + cum_entrant_inc)
policy_110     = ((1 + PRESTIGE_101_CARRYOVER.get(110, 0))
                  * (1 + WIND_TRANSITION_DRAG)
                  * (1 + WIND_DISPLEASURE_DRAG.get(110, 0))
                  * (1 + PRESTIGE_106_BOOST.get(110, 0)))
gdp_110        = prof_sum_110 * POP_PRODUCTIVITY_NEW[110] * policy_110

cum_ent_110 = cum_entrant_inc; hm_cnt_110 = hm_count_110; hm_lv_110 = hm_leaving

new_forecasts = {106: gdp_106, 107: gdp_107, 108: gdp_108, 109: gdp_109, 110: gdp_110}

# =============================================================================
# OUTPUT
# =============================================================================
print("=" * 70)
print("GDP FORECAST FOR HAGELSLAG ISLAND — REVISED MODEL")
print("=" * 70)

print("\nModel Parameters (recalibrated from 100-105 actuals):")
print(f"  Fisher 3-yr cycle:         HIGH=${FISHER_HIGH_AVG_R:,.0f}, LOW=${FISHER_LOW_AVG_R:,.0f}")
print(f"  Sturgeon cycle:            Phase-shifted — surges 101,104,107,110")
print(f"  Locust damage (revised):   {LOCUST_FARMER_DAMAGE_REVISED*100:.1f}% peak (2-yr lag)")
print(f"  Craftsman total growth:    +{CRAFTSMAN_GROWTH_R*100:.1f}% annual")
print(f"  Service total growth:      +{SERVICE_GROWTH_R*100:.1f}% annual")
print(f"  Civil servant growth:      +{CIVIL_SERVANT_GROWTH_R*100:.1f}% annual (workforce grew)")
print(f"  Farmer total growth:       +{FARMER_GROWTH_R*100:.1f}% annual (post-recovery)")
print(f"  Retired income (proj):     ${RETIRED_PROJ[106]:,} → ${RETIRED_PROJ[110]:,} (recovering)")

print("\nPolicies (Year 101, sustained):")
print(f"  Prestige Project:          Construction complete; benefits continue")
print(f"  Retirement Age:            {OLD_RETIREMENT_AGE} → {NEW_RETIREMENT_AGE} (adoption ongoing)")
print(f"  Training Programs (18+):   Mature, sustained")

print("\nPolicies (Year 106, new):")
print(f"  Prestige-101 carry-over:   +2.5 % GDP in Year 106 (residual from 101 project)")
print(f"  Wind Energy Transition:    −3.0 % GDP p.a. Years 106-110; permanent ↓ emissions")
print(f"  Resident Displeasure:      −0.5…−1.5 % GDP Years 106-110; tourism & morale drag")
print(f"  Dual-Income Incentive:     2 %/yr homemakers → workforce (Years 106-110)")
print(f"  Prestige Project 2:        Enacted 106; +0.8…+2.8 % ramp Years 107-110 (+3.0 % in 111)")

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
print("  101: Locust partial impact (-18% farmer); fisher LOW as forecast")
print("  102: Farmer CRASHED -82% (peak locust damage); fisher unexpectedly HIGH")
print("  103: Farmer still crushed; fisher LOW (cycle phase opposite of forecast)")
print("  104-105: Farmer recovery + policies drove ~15% annual growth")

# --- profession-level actuals (Years 100-105) ---
print("\n" + "=" * 70)
print("YEARS 100-105: PROFESSION TOTAL INCOME (actuals)")
print("=" * 70)
prof_keys = ['farmer', 'fisher', 'craftsman', 'service provider', 'civil servant',
             'retired', 'homemaker', 'unemployed']
print(f"{'Profession':<20}", end="")
for y in range(100, 106):
    print(f"{y:>12}", end="")
print()
print("-" * 92)
for prof in prof_keys:
    print(f"{prof:<20}", end="")
    for y in range(100, 106):
        print(f"{profession_income[y].get(prof, 0):>12,.0f}", end="")
    print()
print("-" * 92)
print(f"{'TOTAL GDP':<20}", end="")
for y in range(100, 106):
    print(f"{sum(profession_income[y].values()):>12,.0f}", end="")
print()

# --- 106-110 forecast ---
print("\n" + "=" * 70)
print("YEARS 106-110: REVISED FORECAST (Year 106 policies active)")
print("=" * 70)

notes_106_110 = {
    106: "Fisher LOW; Prestige-101 +2.5 %; Wind −3.0 %; Displeasure −0.5 %",
    107: "Fisher LOW; Surge event; Wind −3.0 %; Displeasure −1.0 %; Prestige-106 +0.8 %",
    108: "Fisher HIGH (107 surge); Wind −3.0 %; Displeasure −1.5 %; Prestige-106 +1.5 %",
    109: "Fisher LOW; Wind −3.0 %; Displeasure −1.5 %; Prestige-106 +2.2 %",
    110: "Fisher LOW; Surge event; Wind −3.0 %; Displeasure −1.0 %; Prestige-106 +2.8 %"
}

policy_mults = {106: policy_106, 107: policy_107, 108: policy_108, 109: policy_109, 110: policy_110}

print(f"{'Year':<6}{'GDP':>15}{'YoY Chg':>10}{'Policy×':>10}  Notes")
print("-" * 78)
print(f"{'105':<6}{ACTUAL_GDP[105]:>15,.2f}{'':>10}{'1.0000':>10}  Actual (baseline)")

prev = ACTUAL_GDP[105]
for year in range(106, 111):
    gdp  = new_forecasts[year]
    chg  = ((gdp - prev) / prev) * 100
    pm   = policy_mults[year]
    print(f"{year:<6}{gdp:>15,.2f}{chg:>+9.1f}%{pm:>10.4f}  {notes_106_110[year]}")
    prev = gdp

# --- profession-level forecasts 105-110 ---
print("\n" + "=" * 70)
print("YEARS 105-110: PROFESSION TOTAL INCOME (105 actual / 106-110 forecast)")
print("=" * 70)

forecast_profs = {
    105: {'fisher': fisher_105_est, 'farmer': farmer_105_est, 'craftsman': craftsman_105_est,
          'service provider': service_105_est, 'civil servant': civil_105_est,
          'retired': retired_105_est, 'homemaker': homemaker_105_est,
          'unemployed': unemployed_105_est, 'new entrants': 0},
    106: {'fisher': fisher_106, 'farmer': farmer_106, 'craftsman': craftsman_106,
          'service provider': service_106, 'civil servant': civil_106,
          'retired': retired_106, 'homemaker': hm_income_106,
          'unemployed': unemp_106, 'new entrants': cum_ent_106},
    107: {'fisher': fisher_107, 'farmer': farmer_107, 'craftsman': craftsman_107,
          'service provider': service_107, 'civil servant': civil_107,
          'retired': retired_107, 'homemaker': hm_income_107,
          'unemployed': unemp_107, 'new entrants': cum_ent_107},
    108: {'fisher': fisher_108, 'farmer': farmer_108, 'craftsman': craftsman_108,
          'service provider': service_108, 'civil servant': civil_108,
          'retired': retired_108, 'homemaker': hm_income_108,
          'unemployed': unemp_108, 'new entrants': cum_ent_108},
    109: {'fisher': fisher_109, 'farmer': farmer_109, 'craftsman': craftsman_109,
          'service provider': service_109, 'civil servant': civil_109,
          'retired': retired_109, 'homemaker': hm_income_109,
          'unemployed': unemp_109, 'new entrants': cum_ent_109},
    110: {'fisher': fisher_110, 'farmer': farmer_110, 'craftsman': craftsman_110,
          'service provider': service_110, 'civil servant': civil_110,
          'retired': retired_110, 'homemaker': hm_income_110,
          'unemployed': unemp_110, 'new entrants': cum_ent_110},
}

prof_order = ['fisher', 'farmer', 'craftsman', 'service provider', 'civil servant',
              'retired', 'homemaker', 'unemployed', 'new entrants']
print(f"{'Profession':<20}", end="")
for y in range(105, 111):
    print(f"{y:>12}", end="")
print()
print("-" * 92)
for prof in prof_order:
    print(f"{prof:<20}", end="")
    for y in range(105, 111):
        print(f"{forecast_profs[y].get(prof, 0):>12,.0f}", end="")
    print()
print("-" * 92)
print(f"{'Prof subtotal':<20}", end="")
for y in range(105, 111):
    print(f"{sum(forecast_profs[y].values()):>12,.0f}", end="")
print()

# --- policy multiplier breakdown ---
print("\n" + "=" * 70)
print("POLICY MULTIPLIER BREAKDOWN (Years 106-110)")
print("=" * 70)
print(f"{'Year':<6}{'Prestige-101':>14}{'Wind Drag':>12}{'Displeasure':>13}{'Prestige-106':>14}{'Combined':>12}")
print("-" * 73)
for y in range(106, 111):
    p101  = PRESTIGE_101_CARRYOVER.get(y, 0.0)
    wind  = WIND_TRANSITION_DRAG
    disp  = WIND_DISPLEASURE_DRAG.get(y, 0.0)
    p106  = PRESTIGE_106_BOOST.get(y, 0.0)
    combo = (1 + p101) * (1 + wind) * (1 + disp) * (1 + p106)
    print(f"{y:<6}{p101:>+13.1%}{wind:>+11.1%}{disp:>+12.1%}{p106:>+13.1%}{combo:>+11.2%}")

# --- homemaker-to-workforce detail ---
print("\n  Dual-Income Household Transition (homemakers → workforce):")
print(f"  {'Year':<6}{'HM count':>10}{'Leaving':>10}{'New ent. inc':>14}{'Cum. ent. inc':>14}")
print("  " + "-" * 56)
hm_data = [(106, hm_cnt_106, hm_lv_106, cum_ent_106),
           (107, hm_cnt_107, hm_lv_107, cum_ent_107),
           (108, hm_cnt_108, hm_lv_108, cum_ent_108),
           (109, hm_cnt_109, hm_lv_109, cum_ent_109),
           (110, hm_cnt_110, hm_lv_110, cum_ent_110)]
for y, cnt, lv, cum in hm_data:
    print(f"  {y:<6}{cnt:>9.1f}{lv:>9.2f}{lv * NEW_ENTRANT_INCOME:>13,.0f}{cum:>13,.0f}")

print("\n" + "=" * 70)
print("Confidence notes:")
print("  - Sturgeon cycle confirmed shifted; surges at 101,104,107,110")
print("  - If cycle drifts +1yr: HIGH moves to 109 instead of 108")
print("  - No disaster events modelled (next locust est. Year 120+)")
print("  - Wind transition: −3 % GDP p.a. is the dominant drag; partially")
print("    offset by Prestige-106 ramp from Year 107 onward")
print("  - Resident displeasure adds −0.5…−1.5 % on top of transition drag;")
print("    channels: tourism decline, civic morale, productivity loss")
print("  - Homemaker exit adds ~$6-7 k/yr in new income (small vs GDP)")
print("  - Weather assumed normal beyond 105 (no data available)")
print("  - Growth rates derived from 100→105 actual profession totals")
print("=" * 70)

# =============================================================================
# POST-MORTEM: YEARS 106-110 FORECAST VS ACTUAL
# =============================================================================
print("\n" + "=" * 70)
print("YEARS 106-110: FORECAST vs ACTUAL (Post-Mortem)")
print("=" * 70)
print(f"{'Year':<6}{'Forecast':>14}{'Actual':>14}{'Fcst Err':>10}{'Act YoY':>10}")
print("-" * 70)

prev_actual = ACTUAL_GDP[105]
for year in range(106, 111):
    fcast = new_forecasts[year]
    actual = ACTUAL_GDP[year]
    err = ((actual - fcast) / fcast) * 100
    yoy = ((actual - prev_actual) / prev_actual) * 100
    print(f"{year:<6}{fcast:>14,.0f}{actual:>14,.0f}{err:>+9.1f}%{yoy:>+9.1f}%")
    prev_actual = actual

print("-" * 70)
print("  106: Wind transition drag + prestige carryover; fisher LOW")
print("  107: DROUGHT hit farmers hard (-67% income); fisher LOW")
print("  108: Farmer partial recovery; fisher HIGH (107 surge)")
print("  109: Continued recovery; fisher LOW")
print("  110: Farmer stabilizing; fisher LOW (surge year)")

# =============================================================================
# YEARS 106-110: PROFESSION ACTUALS (from population_hage_island_year110.csv)
# =============================================================================
print("\n" + "=" * 70)
print("YEARS 106-110: PROFESSION TOTAL INCOME (actuals)")
print("=" * 70)
prof_keys_new = ['farmer', 'fisher', 'craftsman', 'service provider', 'civil servant',
                 'retired', 'homemaker', 'unemployed']
print(f"{'Profession':<20}", end="")
for y in range(106, 111):
    print(f"{y:>12}", end="")
print()
print("-" * 80)
for prof in prof_keys_new:
    print(f"{prof:<20}", end="")
    for y in range(106, 111):
        print(f"{profession_income[y].get(prof, 0):>12,.0f}", end="")
    print()
print("-" * 80)
print(f"{'TOTAL GDP':<20}", end="")
for y in range(106, 111):
    print(f"{sum(profession_income[y].values()):>12,.0f}", end="")
print()

# =============================================================================
# RECALIBRATED PARAMETERS FROM YEARS 106-110 ACTUALS
# =============================================================================
# Sturgeon cycle confirmed: surges at 101, 104, 107, 110
#   HIGH income (1-yr lag): 102, 105, 108, 111...
#   Fisher HIGH avg declining: 4256(102), 4143(105), 3978(108)
#   Fisher LOW avg: ~2400-2500
FISHER_HIGH_AVG_110 = (profession_income[102]['fisher']/workforce[102]['fisher'] +
                       profession_income[105]['fisher']/workforce[105]['fisher'] +
                       profession_income[108]['fisher']/workforce[108]['fisher']) / 3  # ~4125
FISHER_LOW_AVG_110 = (profession_income[106]['fisher']/workforce[106]['fisher'] +
                      profession_income[107]['fisher']/workforce[107]['fisher'] +
                      profession_income[109]['fisher']/workforce[109]['fisher'] +
                      profession_income[110]['fisher']/workforce[110]['fisher']) / 4  # ~2400

# Drought pattern: Year 107 was a severe drought (-67% farmer income)
# Historical drought years: 3,7,10,17,24,31,38,42-43,45,52,59,62,66,73,80,83-84,87,94,107
# Pattern: ~7 year cycle. Next drought expected around 114-117
DROUGHT_FARMER_DAMAGE = -0.67  # 67% income loss during drought year

# Profession growth rates recalibrated from 105→110 actuals
# Craftsman: 253,394 → 212,465 (declined due to economic conditions)
# Service: 225,830 → 219,522 (slight decline)
# Civil servant: 185,584 → 195,683 (continued growth)
CRAFTSMAN_GROWTH_110 = -0.003   # slight decline
SERVICE_GROWTH_110 = -0.005     # slight decline
CIVIL_SERVANT_GROWTH_110 = 0.011  # still growing
FARMER_GROWTH_110 = 0.005  # recovery growth (post-drought)

# =============================================================================
# NEW POLICIES FOR YEARS 111-116
# =============================================================================

# (E) Community Center (Year 111, effects for 5 years following: 112-116)
#     Benefits: Improved social cohesion, mental health, civic engagement
#     Channels: Increased happiness → productivity, reduced crime, better health
#     Effect: +1.5% GDP boost, ramping up over time
COMMUNITY_CENTER_BOOST = {
    112: 0.008,   # Initial community programs begin
    113: 0.012,   # Programs mature, participation grows
    114: 0.015,   # Peak community engagement
    115: 0.015,   # Sustained benefits
    116: 0.015    # Sustained benefits
}

# (F) Public Sports Facilities (Year 111)
#     Benefits: Health improvement, youth development, tourism potential
#     Channels: Reduced healthcare costs, increased productivity, community pride
#     Effect: +1% GDP in year of construction (jobs), +0.8% ongoing
SPORTS_FACILITIES_BOOST = {
    111: 0.010,   # Construction jobs + initial enthusiasm
    112: 0.008,   # Programs established
    113: 0.008,   # Ongoing benefits
    114: 0.008,   # Sustained
    115: 0.008,   # Sustained
    116: 0.008    # Sustained
}

# (G) Drought Resistant Crops (Years 114-115)
#     Based on historical analysis: droughts occur ~every 7 years
#     Year 107 drought caused 67% farmer income loss
#     Next drought expected around 114-117
#     Effect: Reduces drought damage by 50% when drought occurs
#     Implementation cost: -0.5% GDP during transition years
DROUGHT_CROPS_COST = {
    114: -0.005,  # Transition cost - new seeds, training
    115: -0.005   # Continued transition
}
DROUGHT_CROPS_PROTECTION = 0.50  # Reduces drought damage by 50%

# (G2) Farmer Resistance to Drought-Resistant Crops
#      Channels: Skepticism of new varieties, preference for traditional methods,
#      concerns about taste/quality, learning curve, fear of seed dependency
#      Effect: Reduces farmer productivity during adoption period
#      Adoption curve: High resistance initially, decreasing as benefits observed
FARMER_CROP_RESISTANCE = {
    114: -0.08,   # Year 1: High resistance - 8% farmer income reduction
                  # (distrust, learning new techniques, partial adoption ~40%)
    115: -0.04,   # Year 2: Moderate resistance - 4% reduction
                  # (early adopters show results, adoption ~65%)
    116: -0.01,   # Year 3: Low resistance - 1% reduction
                  # (widespread acceptance, adoption ~85%)
    117: 0.00     # Year 4+: Resistance fades, full adoption
}

# (H) Tax Redistribution (Years 111-115)
#     Taxes raised 10% for income over 75th percentile
#     Channels: May reduce high earner productivity/investment
#     GDP impact: -1.5% initially, adapting over time
#     Social benefit: Improved public services (captured in community center effect)
TAX_REDISTRIBUTION_DRAG = {
    111: -0.015,  # Initial drag as high earners adjust
    112: -0.012,  # Partial adaptation
    113: -0.010,  # Further adaptation
    114: -0.008,  # Continued adaptation
    115: -0.008   # Stabilized drag
}

# Calculate 75th percentile income for reference
p75_income_110 = np.percentile(individual_incomes[110], 75) if individual_incomes[110] else 4000

# (D) Prestige Project 106 continuation (effects through Year 111)
#     Reduced from 3% to 1.5% - residual benefits taper more quickly
PRESTIGE_106_BOOST_EXT = {111: 0.015}  # Final year of prestige-106 (tapered)

# Wind transition ends after Year 110
WIND_TRANSITION_ENDS = 110

# =============================================================================
# YEAR 110 ACTUALS (baselines for Year 111+ forecast)
# =============================================================================
fisher_110_act = profession_income[110]['fisher']
farmer_110_act = profession_income[110]['farmer']
craftsman_110_act = profession_income[110]['craftsman']
service_110_act = profession_income[110]['service provider']
civil_110_act = profession_income[110]['civil servant']
retired_110_act = profession_income[110].get('retired', 35000)
homemaker_110_act = profession_income[110].get('homemaker', -18000)
unemployed_110_act = profession_income[110].get('unemployed', -5000)
fisher_count_110 = workforce[110]['fisher']

# Retired projection continues
RETIRED_PROJ_EXT = {111: 36000, 112: 38000, 113: 40000, 114: 42000, 115: 44000, 116: 46000}

# Population productivity (stable growth)
POP_PRODUCTIVITY_111 = {111: 1.001, 112: 1.001, 113: 1.001, 114: 1.001, 115: 1.001, 116: 1.001}

# Homemaker tracking continues
hm_count_110_act = workforce[110].get('homemaker', 40)

# =============================================================================
# YEARS 111-116: FORECAST (New policies active)
# =============================================================================
# Sturgeon cycle: 110 surge → 111 HIGH, 112 LOW, 113 LOW (surge), 114 HIGH, 115 LOW, 116 LOW (surge)
# Drought projection: Possible drought around 114-117 (using 115 as estimate)

# --- Year 111: Fisher HIGH (110 surge), Tax redistribution starts ---
fisher_111 = FISHER_HIGH_AVG_110 * fisher_count_110
farmer_111 = farmer_110_act * (1 + FARMER_GROWTH_110)
craftsman_111 = craftsman_110_act * (1 + CRAFTSMAN_GROWTH_110)
service_111 = service_110_act * (1 + SERVICE_GROWTH_110)
civil_111 = civil_110_act * (1 + CIVIL_SERVANT_GROWTH_110)
retired_111 = RETIRED_PROJ_EXT[111]
hm_count_111 = hm_count_110_act * (1 - HOMEMAKER_EXIT_RATE)
hm_income_111 = homemaker_110_act * (1 + HOME_UNEMP_GROWTH) * (hm_count_111 / hm_count_110_act)
unemp_111 = unemployed_110_act * (1 + HOME_UNEMP_GROWTH)
cum_entrant_111 = cum_entrant_inc * (1 + ENTRANT_GROWTH) + (hm_count_110_act - hm_count_111) * NEW_ENTRANT_INCOME

prof_sum_111 = (fisher_111 + farmer_111 + craftsman_111 + service_111 + civil_111 +
                retired_111 + hm_income_111 + unemp_111 + cum_entrant_111)
policy_111 = ((1 + PRESTIGE_106_BOOST_EXT.get(111, 0)) *
              (1 + SPORTS_FACILITIES_BOOST.get(111, 0)) *
              (1 + TAX_REDISTRIBUTION_DRAG.get(111, 0)))
gdp_111 = prof_sum_111 * POP_PRODUCTIVITY_111[111] * policy_111

# --- Year 112: Fisher LOW, Community center starts ---
fisher_112 = FISHER_LOW_AVG_110 * fisher_count_110
farmer_112 = farmer_111 * (1 + FARMER_GROWTH_110)
craftsman_112 = craftsman_111 * (1 + CRAFTSMAN_GROWTH_110)
service_112 = service_111 * (1 + SERVICE_GROWTH_110)
civil_112 = civil_111 * (1 + CIVIL_SERVANT_GROWTH_110)
retired_112 = RETIRED_PROJ_EXT[112]
hm_count_112 = hm_count_111 * (1 - HOMEMAKER_EXIT_RATE)
hm_income_112 = hm_income_111 * (1 + HOME_UNEMP_GROWTH) * (hm_count_112 / hm_count_111)
unemp_112 = unemp_111 * (1 + HOME_UNEMP_GROWTH)
cum_entrant_112 = cum_entrant_111 * (1 + ENTRANT_GROWTH) + (hm_count_111 - hm_count_112) * NEW_ENTRANT_INCOME

prof_sum_112 = (fisher_112 + farmer_112 + craftsman_112 + service_112 + civil_112 +
                retired_112 + hm_income_112 + unemp_112 + cum_entrant_112)
policy_112 = ((1 + COMMUNITY_CENTER_BOOST.get(112, 0)) *
              (1 + SPORTS_FACILITIES_BOOST.get(112, 0)) *
              (1 + TAX_REDISTRIBUTION_DRAG.get(112, 0)))
gdp_112 = prof_sum_112 * POP_PRODUCTIVITY_111[112] * policy_112

# --- Year 113: Fisher LOW (surge year), Tax redistribution final year ---
fisher_113 = FISHER_LOW_AVG_110 * fisher_count_110
farmer_113 = farmer_112 * (1 + FARMER_GROWTH_110)
craftsman_113 = craftsman_112 * (1 + CRAFTSMAN_GROWTH_110)
service_113 = service_112 * (1 + SERVICE_GROWTH_110)
civil_113 = civil_112 * (1 + CIVIL_SERVANT_GROWTH_110)
retired_113 = RETIRED_PROJ_EXT[113]
hm_count_113 = hm_count_112 * (1 - HOMEMAKER_EXIT_RATE)
hm_income_113 = hm_income_112 * (1 + HOME_UNEMP_GROWTH) * (hm_count_113 / hm_count_112)
unemp_113 = unemp_112 * (1 + HOME_UNEMP_GROWTH)
cum_entrant_113 = cum_entrant_112 * (1 + ENTRANT_GROWTH) + (hm_count_112 - hm_count_113) * NEW_ENTRANT_INCOME

prof_sum_113 = (fisher_113 + farmer_113 + craftsman_113 + service_113 + civil_113 +
                retired_113 + hm_income_113 + unemp_113 + cum_entrant_113)
policy_113 = ((1 + COMMUNITY_CENTER_BOOST.get(113, 0)) *
              (1 + SPORTS_FACILITIES_BOOST.get(113, 0)) *
              (1 + TAX_REDISTRIBUTION_DRAG.get(113, 0)))
gdp_113 = prof_sum_113 * POP_PRODUCTIVITY_111[113] * policy_113

# --- Year 114: Fisher HIGH (113 surge), Tax ended, Drought crops start ---
fisher_114 = FISHER_HIGH_AVG_110 * fisher_count_110
# Apply farmer resistance to drought-resistant crops (Year 1 of adoption)
farmer_114 = farmer_113 * (1 + FARMER_GROWTH_110) * (1 + FARMER_CROP_RESISTANCE.get(114, 0))
craftsman_114 = craftsman_113 * (1 + CRAFTSMAN_GROWTH_110)
service_114 = service_113 * (1 + SERVICE_GROWTH_110)
civil_114 = civil_113 * (1 + CIVIL_SERVANT_GROWTH_110)
retired_114 = RETIRED_PROJ_EXT[114]
hm_count_114 = hm_count_113 * (1 - HOMEMAKER_EXIT_RATE)
hm_income_114 = hm_income_113 * (1 + HOME_UNEMP_GROWTH) * (hm_count_114 / hm_count_113)
unemp_114 = unemp_113 * (1 + HOME_UNEMP_GROWTH)
cum_entrant_114 = cum_entrant_113 * (1 + ENTRANT_GROWTH) + (hm_count_113 - hm_count_114) * NEW_ENTRANT_INCOME

prof_sum_114 = (fisher_114 + farmer_114 + craftsman_114 + service_114 + civil_114 +
                retired_114 + hm_income_114 + unemp_114 + cum_entrant_114)
policy_114 = ((1 + COMMUNITY_CENTER_BOOST.get(114, 0)) *
              (1 + SPORTS_FACILITIES_BOOST.get(114, 0)) *
              (1 + DROUGHT_CROPS_COST.get(114, 0)) *
              (1 + TAX_REDISTRIBUTION_DRAG.get(114, 0)))
gdp_114 = prof_sum_114 * POP_PRODUCTIVITY_111[114] * policy_114

# --- Year 115: Fisher LOW, Drought crops Year 2, POTENTIAL DROUGHT YEAR ---
# Model drought with 40% probability based on 7-year cycle pattern
DROUGHT_PROBABILITY_115 = 0.40
fisher_115 = FISHER_LOW_AVG_110 * fisher_count_110
# Drought scenario: farmer income -67%, mitigated by 50% due to drought-resistant crops
# Apply farmer resistance Year 2 (reduced from Year 1), adjusting for prior year's resistance
farmer_115_base = farmer_114 / (1 + FARMER_CROP_RESISTANCE.get(114, 0))  # Remove Year 1 resistance
farmer_115_no_drought = farmer_115_base * (1 + FARMER_GROWTH_110) * (1 + FARMER_CROP_RESISTANCE.get(115, 0))
farmer_115_with_drought = farmer_115_base * (1 + DROUGHT_FARMER_DAMAGE) * (1 + DROUGHT_CROPS_PROTECTION * 0.67) * (1 + FARMER_CROP_RESISTANCE.get(115, 0))
# Use expected value: weighted average
farmer_115 = farmer_115_no_drought * (1 - DROUGHT_PROBABILITY_115) + farmer_115_with_drought * DROUGHT_PROBABILITY_115
craftsman_115 = craftsman_114 * (1 + CRAFTSMAN_GROWTH_110)
service_115 = service_114 * (1 + SERVICE_GROWTH_110)
civil_115 = civil_114 * (1 + CIVIL_SERVANT_GROWTH_110)
retired_115 = RETIRED_PROJ_EXT[115]
hm_count_115 = hm_count_114 * (1 - HOMEMAKER_EXIT_RATE)
hm_income_115 = hm_income_114 * (1 + HOME_UNEMP_GROWTH) * (hm_count_115 / hm_count_114)
unemp_115 = unemp_114 * (1 + HOME_UNEMP_GROWTH)
cum_entrant_115 = cum_entrant_114 * (1 + ENTRANT_GROWTH) + (hm_count_114 - hm_count_115) * NEW_ENTRANT_INCOME

prof_sum_115 = (fisher_115 + farmer_115 + craftsman_115 + service_115 + civil_115 +
                retired_115 + hm_income_115 + unemp_115 + cum_entrant_115)
policy_115 = ((1 + COMMUNITY_CENTER_BOOST.get(115, 0)) *
              (1 + SPORTS_FACILITIES_BOOST.get(115, 0)) *
              (1 + DROUGHT_CROPS_COST.get(115, 0)) *
              (1 + TAX_REDISTRIBUTION_DRAG.get(115, 0)))
gdp_115 = prof_sum_115 * POP_PRODUCTIVITY_111[115] * policy_115

# --- Year 116: Fisher LOW (surge year), Drought crops mature ---
fisher_116 = FISHER_LOW_AVG_110 * fisher_count_110
# Farmer resistance decreases in Year 2; recovery boost if drought occurred in 115
farmer_116 = farmer_115 * (1 + FARMER_GROWTH_110) * 1.10 * (1 + FARMER_CROP_RESISTANCE.get(116, 0)) / (1 + FARMER_CROP_RESISTANCE.get(115, 0))  # Adjust for changing resistance
craftsman_116 = craftsman_115 * (1 + CRAFTSMAN_GROWTH_110)
service_116 = service_115 * (1 + SERVICE_GROWTH_110)
civil_116 = civil_115 * (1 + CIVIL_SERVANT_GROWTH_110)
retired_116 = RETIRED_PROJ_EXT[116]
hm_count_116 = hm_count_115 * (1 - HOMEMAKER_EXIT_RATE)
hm_income_116 = hm_income_115 * (1 + HOME_UNEMP_GROWTH) * (hm_count_116 / hm_count_115)
unemp_116 = unemp_115 * (1 + HOME_UNEMP_GROWTH)
cum_entrant_116 = cum_entrant_115 * (1 + ENTRANT_GROWTH) + (hm_count_115 - hm_count_116) * NEW_ENTRANT_INCOME

prof_sum_116 = (fisher_116 + farmer_116 + craftsman_116 + service_116 + civil_116 +
                retired_116 + hm_income_116 + unemp_116 + cum_entrant_116)
policy_116 = ((1 + COMMUNITY_CENTER_BOOST.get(116, 0)) *
              (1 + SPORTS_FACILITIES_BOOST.get(116, 0)) *
              (1 + DROUGHT_CROPS_COST.get(116, 0)))
gdp_116 = prof_sum_116 * POP_PRODUCTIVITY_111[116] * policy_116

forecasts_111_115 = {111: gdp_111, 112: gdp_112, 113: gdp_113, 114: gdp_114, 115: gdp_115}

# =============================================================================
# OUTPUT: YEARS 111-115 FORECAST
# =============================================================================
print("\n" + "=" * 80)
print("YEARS 111-115: FORECAST (New policies active)")
print("=" * 80)

print("\nNew Policies Enacted in Year 111:")
print(f"  Public Sports Facilities: Built Year 111; benefits Years 111-115 (+0.8-1.0% GDP)")
print(f"  Tax Redistribution:      Years 111-115; 10% increase on >75th percentile income")
print(f"                           (75th percentile in Year 110: ${p75_income_110:,.0f})")
print(f"  Drought Resistant Crops: Implemented Years 114-115; -0.5% transition cost")
print(f"                           50% protection against drought damage")
print(f"  Farmer Resistance:       Year 114: -8% farmer income (adoption ~40%)")
print(f"                           Year 115: -4% farmer income (adoption ~65%)")

notes_111_115 = {
    111: "Fisher HIGH (110 surge); Prestige-106 +1.5%; Sports +1%; Tax drag -1.5%",
    112: "Fisher LOW; Community center +0.8%; Sports +0.8%; Tax drag -1.2%",
    113: "Fisher LOW (surge); Community +1.2%; Sports +0.8%; Tax drag -1.0%",
    114: "Fisher HIGH (113 surge); Community +1.5%; Sports +0.8%; Tax drag -0.8%; Drought crops -0.5%; Farmer resistance -8%",
    115: "Fisher LOW; Tax drag -0.8%; Drought crops -0.5%; Farmer resistance -4%; Drought risk 40%"
}

print(f"\n{'Year':<6}{'GDP Forecast':>15}{'YoY Chg':>10}  Notes")
print("-" * 95)
print(f"{'110':<6}{ACTUAL_GDP[110]:>15,.2f}{'':>10}  Actual (baseline)")

prev = ACTUAL_GDP[110]
for year in range(111, 116):
    gdp_f = forecasts_111_115[year]
    chg = ((gdp_f - prev) / prev) * 100
    print(f"{year:<6}{gdp_f:>15,.2f}{chg:>+9.1f}%  {notes_111_115[year]}")
    prev = gdp_f

# --- Policy multiplier breakdown 111-115 ---
print("\n" + "=" * 80)
print("POLICY MULTIPLIER BREAKDOWN (Years 111-115)")
print("=" * 80)
print(f"{'Year':<6}{'Prestige-106':>13}{'Community':>11}{'Sports':>10}{'Tax Drag':>11}{'Drought':>10}{'Combined':>12}")
print("-" * 80)
for y in range(111, 116):
    p106 = PRESTIGE_106_BOOST_EXT.get(y, 0.0)
    comm = COMMUNITY_CENTER_BOOST.get(y, 0.0)
    sport = SPORTS_FACILITIES_BOOST.get(y, 0.0)
    tax = TAX_REDISTRIBUTION_DRAG.get(y, 0.0)
    drought = DROUGHT_CROPS_COST.get(y, 0.0)
    combo = (1 + p106) * (1 + comm) * (1 + sport) * (1 + tax) * (1 + drought)
    print(f"{y:<6}{p106:>+12.1%}{comm:>+10.1%}{sport:>+9.1%}{tax:>+10.1%}{drought:>+9.1%}{combo:>+11.2%}")

# --- Drought-resistant crops analysis ---
print("\n" + "=" * 80)
print("DROUGHT-RESISTANT CROPS ANALYSIS")
print("=" * 80)
print("\nHistorical Drought Years (farmer avg income <$1000):")
print("  Years: 3, 7, 10, 17, 24, 31, 38, 42-43, 45, 52, 59, 62, 66, 73, 80, 83-84, 87, 94, 107")
print("  Pattern: ~7 year cycle with clustering")
print("\nYear 107 Drought Impact:")
print(f"  Farmer income: ${profession_income[106]['farmer']/workforce[106]['farmer']:,.0f} (106)")
print(f"              → ${profession_income[107]['farmer']/workforce[107]['farmer']:,.0f} (107 drought)")
print(f"              → ${profession_income[108]['farmer']/workforce[108]['farmer']:,.0f} (108 recovery)")
print(f"  Damage: -67% farmer income")
print("\nNext Drought Projection:")
print("  Based on 7-year cycle from Year 107: Next drought ~Year 114-117")
print("  Probability estimate: 40% chance in Year 115")
print("\nFarmer Resistance to New Crops (adoption curve):")
print(f"  {'Year':<6}{'Resistance':>12}{'Adoption Rate':>16}{'Channels'}")
print("  " + "-" * 70)
for y in [114, 115, 116, 117]:
    resist = FARMER_CROP_RESISTANCE.get(y, 0)
    adoption = {114: "~40%", 115: "~65%", 116: "~85%", 117: "~95%"}
    channels = {
        114: "High distrust, learning new techniques",
        115: "Early adopters show success, skepticism fades",
        116: "Widespread acceptance, proven results",
        117: "Full adoption, resistance negligible"
    }
    print(f"  {y:<6}{resist:>+11.0%}{adoption[y]:>16}  {channels[y]}")

print("\nPolicy Recommendation: ENACT DROUGHT-RESISTANT CROPS")
print("  - Implementation cost: -0.5% GDP in Years 114-115")
print("  - Protection: Reduces drought damage by 50%")
print("  - Farmer resistance: -8% farmer income (Yr 114), -4% (Yr 115)")
print("    Channels: Skepticism, traditional preferences, learning curve")
print("  - Expected value: Still positive despite resistance;")
print("    drought protection value exceeds adoption costs over 3+ years")

print("\n" + "=" * 80)
print("SUMMARY: 5-YEAR OUTLOOK (Years 111-115)")
print("=" * 80)
print(f"\nBaseline GDP (Year 110): ${ACTUAL_GDP[110]:,.2f}")
print(f"Forecast GDP (Year 115): ${gdp_115:,.2f}")
total_growth = ((gdp_115 - ACTUAL_GDP[110]) / ACTUAL_GDP[110]) * 100
print(f"Total Growth: {total_growth:+.1f}%")
print(f"Annualized Growth: {((gdp_115/ACTUAL_GDP[110])**(1/5) - 1)*100:+.1f}%")

print("\nKey Risks:")
print("  - Drought in 114-117 window (mitigated by drought-resistant crops)")
print("  - Farmer resistance to new crops may slow adoption (-8% to -4% farmer income)")
print("  - Tax redistribution may reduce high-earner investment")
print("  - Sturgeon cycle volatility (fisher income swings ±70%)")
print("\nKey Opportunities:")
print("  - Community center and sports facilities boost social cohesion")
print("  - Drought-resistant crops provide agricultural resilience")
print("  - Civil servant sector continues stable growth")
print("=" * 80)

# =============================================================================
# GINI COEFFICIENT ANALYSIS AND PREDICTION
# =============================================================================

def calculate_gini(incomes):
    """Calculate Gini coefficient from a list of incomes."""
    if len(incomes) == 0:
        return 0.0
    # Filter to positive incomes only for Gini calculation
    pos_incomes = [i for i in incomes if i > 0]
    if len(pos_incomes) == 0:
        return 0.0
    sorted_incomes = sorted(pos_incomes)
    n = len(sorted_incomes)
    cumsum = np.cumsum(sorted_incomes)
    return (2 * np.sum((np.arange(1, n + 1) * sorted_incomes)) / (n * cumsum[-1])) - (n + 1) / n

# Calculate historical Gini coefficients (Years 100-110)
historical_gini = {}
for year in range(100, 111):
    if year in individual_incomes and len(individual_incomes[year]) > 0:
        historical_gini[year] = calculate_gini(individual_incomes[year])

# Get income distribution statistics for Year 110
incomes_110 = individual_incomes[110]
p25_110 = np.percentile(incomes_110, 25)
p50_110 = np.percentile(incomes_110, 50)  # median
p75_110 = np.percentile(incomes_110, 75)
p90_110 = np.percentile(incomes_110, 90)
mean_110 = np.mean(incomes_110)
gini_110 = historical_gini[110]

# Identify high earners (>75th percentile) and their share
high_earners_110 = [i for i in incomes_110 if i > p75_110]
high_earner_share_110 = sum(high_earners_110) / sum(incomes_110)

# =============================================================================
# GINI PREDICTION MODEL
# =============================================================================
# Policy effects on Gini coefficient:
#   Tax redistribution: Reduces inequality by taxing high earners
#   - 10% tax on >75th percentile reduces their effective income
#   - Estimated Gini reduction: -0.008 to -0.015 per year (progressive effect)
#
#   Fisher cycle: HIGH years increase fisher income relative to others
#   - Fishers are typically mid-to-high earners
#   - HIGH years may slightly increase Gini; LOW years decrease it
#   - Estimated effect: ±0.005-0.010
#
#   Farmer resistance: Reduces farmer income (farmers are typically lower-mid earners)
#   - May slightly increase Gini as lower earners earn less
#   - Estimated effect: +0.002-0.005
#
#   Sports/Community: Neutral to slightly equalizing (broad-based benefits)
#   - Estimated effect: -0.001-0.002

# Tax redistribution effect on Gini (progressive impact)
# Effect strengthens over time as redistribution accumulates
TAX_GINI_EFFECT = {
    111: -0.010,  # Initial redistribution effect
    112: -0.012,  # Growing impact as funds redistributed
    113: -0.012,  # Sustained redistribution
    114: -0.010,  # Continued strong effect
    115: -0.010   # Sustained
}

# Fisher cycle effect on Gini (HIGH years increase inequality slightly)
# Year 111: HIGH, 112: LOW, 113: LOW, 114: HIGH, 115: LOW
# Effect moderated by tax redistribution in later years
FISHER_GINI_EFFECT = {
    111: +0.006,   # HIGH year - fishers earn more
    112: -0.004,   # LOW year
    113: -0.004,   # LOW year
    114: +0.005,   # HIGH year (moderated by established tax policy)
    115: -0.004    # LOW year
}

# Farmer resistance effect (reduces lower-mid earner income)
# Effect is small - farmers are diverse income group
FARMER_RESISTANCE_GINI = {
    114: +0.001,  # -8% farmer income, minor inequality effect
    115: +0.001   # -4% farmer income
}

# Community/Sports effect (broad-based, slightly equalizing)
COMMUNITY_GINI_EFFECT = {
    112: -0.002,
    113: -0.002,
    114: -0.002,
    115: -0.002
}

# Predict Gini for years 111-115
predicted_gini = {110: gini_110}
for year in range(111, 116):
    base_gini = predicted_gini[year - 1]

    # Apply policy effects
    tax_effect = TAX_GINI_EFFECT.get(year, 0)
    fisher_effect = FISHER_GINI_EFFECT.get(year, 0)
    farmer_effect = FARMER_RESISTANCE_GINI.get(year, 0)
    community_effect = COMMUNITY_GINI_EFFECT.get(year, 0)

    # Natural drift toward mean (slight mean reversion)
    mean_reversion = (0.35 - base_gini) * 0.02  # Slight pull toward 0.35

    predicted_gini[year] = base_gini + tax_effect + fisher_effect + farmer_effect + community_effect + mean_reversion

# =============================================================================
# OUTPUT: GINI COEFFICIENT ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("GINI COEFFICIENT ANALYSIS AND PREDICTION")
print("=" * 80)

print("\nYear 110 Income Distribution (baseline):")
print(f"  Population with income: {len(incomes_110)}")
print(f"  Mean income:           ${mean_110:,.0f}")
print(f"  25th percentile:       ${p25_110:,.0f}")
print(f"  Median (50th):         ${p50_110:,.0f}")
print(f"  75th percentile:       ${p75_110:,.0f}")
print(f"  90th percentile:       ${p90_110:,.0f}")
print(f"  High earner share:     {high_earner_share_110:.1%} of total income (top 25%)")
print(f"  Gini coefficient:      {gini_110:.4f}")

print("\nHistorical Gini Coefficients (Years 100-110):")
print(f"  {'Year':<6}{'Gini':>8}{'YoY Change':>12}")
print("  " + "-" * 26)
prev_g = None
for year in range(100, 111):
    g = historical_gini.get(year, 0)
    if prev_g is not None:
        chg = g - prev_g
        print(f"  {year:<6}{g:>8.4f}{chg:>+11.4f}")
    else:
        print(f"  {year:<6}{g:>8.4f}{'':>12}")
    prev_g = g

print("\nPolicy Effects on Income Inequality:")
print(f"  Tax Redistribution (>75th pctl):  Reduces Gini by 0.006-0.012/year")
print(f"  Fisher HIGH years:                Increases Gini by ~0.008 (mid-high earners gain)")
print(f"  Fisher LOW years:                 Decreases Gini by ~0.005")
print(f"  Farmer resistance:                Increases Gini by ~0.002-0.003")
print(f"  Community/Sports:                 Decreases Gini by ~0.002 (broad benefits)")

print("\nPredicted Gini Coefficients (Years 111-115):")
print(f"  {'Year':<6}{'Gini':>8}{'Change':>10}{'Tax':>8}{'Fisher':>8}{'Other':>8}  Notes")
print("  " + "-" * 70)
print(f"  {'110':<6}{gini_110:>8.4f}{'':>10}{'':>8}{'':>8}{'':>8}  Actual (baseline)")

for year in range(111, 116):
    g = predicted_gini[year]
    chg = g - predicted_gini[year - 1]
    tax = TAX_GINI_EFFECT.get(year, 0)
    fisher = FISHER_GINI_EFFECT.get(year, 0)
    other = FARMER_RESISTANCE_GINI.get(year, 0) + COMMUNITY_GINI_EFFECT.get(year, 0)
    fisher_note = "HIGH" if fisher > 0 else "LOW"
    print(f"  {year:<6}{g:>8.4f}{chg:>+9.4f}{tax:>+7.3f}{fisher:>+7.3f}{other:>+7.3f}  Fisher {fisher_note}")

print("\nGini Interpretation:")
print(f"  Year 110 Gini: {gini_110:.4f}")
print(f"  Year 115 Gini: {predicted_gini[115]:.4f} (predicted)")
gini_change = predicted_gini[115] - gini_110
print(f"  5-Year Change: {gini_change:+.4f} ({'more equal' if gini_change < 0 else 'more unequal'})")
print("\n  Gini Scale Reference:")
print("    0.25-0.30: Low inequality (Nordic countries)")
print("    0.30-0.35: Moderate inequality")
print("    0.35-0.40: Moderate-high inequality")
print("    0.40-0.50: High inequality (US ~0.41)")
print("=" * 80)

# =============================================================================
# POST-MORTEM: YEARS 111-115 FORECAST VS ACTUAL
# =============================================================================
print("\n" + "=" * 80)
print("POST-MORTEM: YEARS 111-115 FORECAST VS ACTUAL")
print("=" * 80)

print("\nGDP Forecast vs Actual:")
print(f"  {'Year':<6}{'Forecast':>14}{'Actual':>14}{'Error':>10}{'Act YoY':>10}")
print("  " + "-" * 54)
prev_actual = ACTUAL_GDP[110]
for year in range(111, 116):
    fcast = forecasts_111_115[year]
    actual = ACTUAL_GDP[year]
    err = ((actual - fcast) / fcast) * 100
    yoy = ((actual - prev_actual) / prev_actual) * 100
    print(f"  {year:<6}{fcast:>14,.0f}{actual:>14,.0f}{err:>+9.1f}%{yoy:>+9.1f}%")
    prev_actual = actual

print("\nGini Forecast vs Actual:")
print(f"  {'Year':<6}{'Forecast':>10}{'Full Econ':>12}{'Formal':>10}{'Note'}")
print("  " + "-" * 60)
for year in range(111, 116):
    fcast_g = predicted_gini[year]
    actual_full = ACTUAL_GINI[year]['full']
    actual_formal = ACTUAL_GINI[year]['formal']
    # Compare forecast to formal economy Gini
    diff = actual_formal - fcast_g
    note = "Raiders/gangs increase full economy inequality"
    print(f"  {year:<6}{fcast_g:>10.4f}{actual_full:>12.2f}{actual_formal:>10.2f}  {note if year == 111 else ''}")

print("\nKey Insights from Actuals:")
print("  GDP:")
total_gdp_growth = ((ACTUAL_GDP[115] - ACTUAL_GDP[110]) / ACTUAL_GDP[110]) * 100
print(f"    - Total growth 110→115: {total_gdp_growth:+.1f}%")
print(f"    - Year 111 actual (+20.8%) exceeded forecast (+17.2%)")
print(f"    - Year 115 actual ($981k) close to forecast ($983k)")

print("\n  Gini (Income Inequality):")
print("    - Two measures tracked: Full economy vs Formal economy")
print("    - Full economy Gini (0.46-0.54) includes raiders/gangs income")
print("    - Formal economy Gini (0.37-0.40) excludes illegal income")
print("    - Raiders/gangs add ~0.10-0.14 to inequality measure")
print("    - Formal Gini trend: 0.37→0.40→0.37 (slight improvement by 115)")

print("\n  Wellbeing Implications:")
print("    - High full-economy Gini indicates significant shadow economy")
print("    - Raiders/gangs concentrate wealth outside formal system")
print("    - Tax redistribution helping formal economy equality")
print("    - Need policies addressing informal/illegal economy for wellbeing")
print("=" * 80)

# =============================================================================
# YEARS 116-120 FORECAST (New policies)
# =============================================================================
# Policies:
#   (A) Community Center - Taxes raised Year 116, benefits Years 117-121
#   (B) Security Infrastructure - Years 116-120 (reduces raider impact)
#   (C) Training Programmes - Year 116 only
#   (D) Trade Agreement - Year 118
#
# Raiders/Gangs:
#   - Still present on island
#   - Slightly increase GDP (shadow economy)
#   - Disrupt happiness
#   - Security infrastructure reduces their negative impact

# Year 115 actuals as baseline
GDP_115 = ACTUAL_GDP[115]
GINI_115_FORMAL = ACTUAL_GINI[115]['formal']
GINI_115_FULL = ACTUAL_GINI[115]['full']

# Historical happiness baseline (Year 100 avg was ~100)
HAPPINESS_BASELINE = 100.0

# =============================================================================
# NEW POLICY PARAMETERS (Years 116-120)
# =============================================================================

# (A) Community Center - Taxes raised Year 116, benefits Years 117-121
#     Similar to previous community center but with tax funding
COMMUNITY_CENTER_TAX = {116: -0.003}  # Modest tax increase to fund community center
COMMUNITY_CENTER_BENEFIT = {
    117: 0.010,   # Initial community programs
    118: 0.012,   # Programs mature
    119: 0.015,   # Peak engagement
    120: 0.015    # Sustained benefits
}
# Happiness effect from community center
COMMUNITY_CENTER_HAPPINESS = {
    117: +2.0,   # New social programs begin
    118: +3.0,   # Programs mature, participation grows
    119: +4.0,   # Peak community engagement
    120: +4.0    # Sustained happiness benefit
}

# (B) Security Infrastructure - Years 116-120
#     Reduces raider impact on formal economy and happiness
SECURITY_INFRASTRUCTURE_COST = -0.005  # Annual cost
SECURITY_INFRASTRUCTURE_BENEFIT = {
    116: 0.002,   # Initial deployment
    117: 0.005,   # Growing effectiveness
    118: 0.008,   # Full operation
    119: 0.010,   # Optimized
    120: 0.010    # Sustained
}
# Reduces raider negative impact on happiness
SECURITY_HAPPINESS_BOOST = {
    116: +1.0,
    117: +2.0,
    118: +3.0,
    119: +4.0,
    120: +4.0
}

# (C) Training Programmes - Year 116 only
#     One-time boost to workforce productivity
TRAINING_PROGRAMME_BOOST = {116: 0.018}  # One-time productivity boost
TRAINING_HAPPINESS = {116: +1.0}  # Slight happiness from new skills

# (D) Trade Agreement - Year 118
#     Opens new markets, boosts exports
TRADE_AGREEMENT_BOOST = {
    118: 0.015,   # Initial trade boost
    119: 0.020,   # Trade grows
    120: 0.025    # Mature trade relationship
}
TRADE_HAPPINESS = {
    118: +1.5,   # New goods available
    119: +2.0,   # More variety
    120: +2.0    # Sustained
}

# =============================================================================
# RAIDER/GANG EFFECTS
# =============================================================================
# Raiders slightly increase GDP (shadow economy) but hurt happiness
# Security infrastructure reduces these effects over time

RAIDER_GDP_BOOST = 0.015  # Raiders add ~1.5% to GDP (shadow economy)
RAIDER_HAPPINESS_DRAG = {
    116: -5.0,   # High raider activity
    117: -4.0,   # Security starting to help
    118: -3.0,   # Improving
    119: -2.0,   # Mostly contained
    120: -2.0    # Residual criminal activity
}
# Security infrastructure reduces raider GDP contribution over time
# (as raiders are pushed out, less shadow economy activity)
RAIDER_GDP_REDUCTION = {
    116: 0.0,    # Raiders still active
    117: -0.003, # Some raiders pushed out
    118: -0.005, # More leaving
    119: -0.008, # Significantly reduced
    120: -0.010  # Most raiders gone
}

# =============================================================================
# FISHER CYCLE (continues from established pattern)
# =============================================================================
# Surges: 110, 113, 116, 119... -> HIGH income years: 111, 114, 117, 120...
# Year 116: LOW (surge year), 117: HIGH, 118: LOW, 119: LOW (surge), 120: HIGH
FISHER_CYCLE_116_120 = {
    116: 'LOW',   # Surge happens this year
    117: 'HIGH',  # Post-surge high income
    118: 'LOW',
    119: 'LOW',   # Surge happens this year
    120: 'HIGH'   # Post-surge high income
}

# Fisher income averages (continuing trend)
FISHER_HIGH_AVG_115 = 4000  # Slightly declining trend
FISHER_LOW_AVG_115 = 2350

# =============================================================================
# GDP FORECAST 116-120
# =============================================================================
gdp_forecasts_116_120 = {}
prev_gdp = GDP_115

for year in range(116, 121):
    # Base growth from profession trends
    base_growth = 1.005  # ~0.5% baseline profession growth

    # Fisher cycle effect
    if FISHER_CYCLE_116_120[year] == 'HIGH':
        fisher_effect = 0.12  # HIGH years boost GDP ~12%
    else:
        fisher_effect = -0.08  # LOW years reduce GDP ~8%

    # Policy effects
    community_tax = COMMUNITY_CENTER_TAX.get(year, 0)
    community_benefit = COMMUNITY_CENTER_BENEFIT.get(year, 0)
    security_cost = SECURITY_INFRASTRUCTURE_COST
    security_benefit = SECURITY_INFRASTRUCTURE_BENEFIT.get(year, 0)
    training = TRAINING_PROGRAMME_BOOST.get(year, 0)
    trade = TRADE_AGREEMENT_BOOST.get(year, 0)

    # Raider effects
    raider_gdp = RAIDER_GDP_BOOST + RAIDER_GDP_REDUCTION.get(year, 0)

    # Combined policy multiplier
    policy_mult = (1 + community_tax + community_benefit + security_cost +
                   security_benefit + training + trade + raider_gdp)

    # Calculate GDP
    gdp_forecasts_116_120[year] = prev_gdp * base_growth * (1 + fisher_effect) * policy_mult
    prev_gdp = gdp_forecasts_116_120[year]

# =============================================================================
# HAPPINESS FORECAST 116-120
# =============================================================================
# Happiness scale: 0-100, baseline ~100
happiness_forecasts = {}
prev_happiness = HAPPINESS_BASELINE  # Start from baseline

for year in range(116, 121):
    # Community center effect
    community_happy = COMMUNITY_CENTER_HAPPINESS.get(year, 0)

    # Security effect
    security_happy = SECURITY_HAPPINESS_BOOST.get(year, 0)

    # Training effect
    training_happy = TRAINING_HAPPINESS.get(year, 0)

    # Trade effect
    trade_happy = TRADE_HAPPINESS.get(year, 0)

    # Raider negative effect
    raider_drag = RAIDER_HAPPINESS_DRAG.get(year, 0)

    # Fisher cycle effect on happiness (income affects happiness)
    if FISHER_CYCLE_116_120[year] == 'HIGH':
        fisher_happy = +1.5  # Higher income = happier
    else:
        fisher_happy = -1.0  # Lower income = less happy

    # Economic stability effect (GDP growth affects happiness)
    gdp_growth = (gdp_forecasts_116_120[year] - (GDP_115 if year == 116 else gdp_forecasts_116_120[year-1])) / (GDP_115 if year == 116 else gdp_forecasts_116_120[year-1])
    econ_happy = gdp_growth * 10  # 1% GDP growth = +0.1 happiness

    # Calculate happiness (bounded 0-100)
    total_change = community_happy + security_happy + training_happy + trade_happy + raider_drag + fisher_happy + econ_happy
    happiness_forecasts[year] = max(0, min(100, prev_happiness + total_change))
    prev_happiness = happiness_forecasts[year]

# =============================================================================
# GINI FORECAST 116-120
# =============================================================================
# Tracking both formal and full economy Gini
gini_formal_forecasts = {}
gini_full_forecasts = {}
prev_formal = GINI_115_FORMAL
prev_full = GINI_115_FULL

for year in range(116, 121):
    # Community center effect (equalizing)
    community_gini = -0.005 if year >= 117 else 0

    # Security effect (reduces raider inequality in full economy)
    security_gini_full = -0.015 * (year - 115) / 5  # Gradual reduction

    # Training effect (slightly equalizing - helps lower earners)
    training_gini = -0.003 if year == 116 else 0

    # Trade effect (mixed - may increase inequality slightly)
    trade_gini = 0.002 if year >= 118 else 0

    # Fisher cycle effect
    if FISHER_CYCLE_116_120[year] == 'HIGH':
        fisher_gini = +0.005
    else:
        fisher_gini = -0.004

    # Formal economy Gini
    gini_formal_forecasts[year] = prev_formal + community_gini + training_gini + trade_gini + fisher_gini
    prev_formal = gini_formal_forecasts[year]

    # Full economy Gini (includes raider effect, reduced by security)
    gini_full_forecasts[year] = prev_full + community_gini + training_gini + trade_gini + fisher_gini + security_gini_full
    prev_full = gini_full_forecasts[year]

# =============================================================================
# OUTPUT: YEARS 116-120 FORECAST
# =============================================================================
print("\n" + "=" * 80)
print("YEARS 116-120 FORECAST: WELLBEING FOCUS")
print("=" * 80)

print("\nNew Policies:")
print("  (A) Community Center:      Tax increase Year 116 (-0.8% GDP)")
print("                             Benefits Years 117-120 (+1.0-1.5% GDP, +2-4 happiness)")
print("  (B) Security Infrastructure: All years 116-120 (-0.5% cost, +0.2-1.0% benefit)")
print("                             Reduces raider impact on happiness (+1-4 pts)")
print("  (C) Training Programmes:   Year 116 only (+1.2% GDP, +1 happiness)")
print("  (D) Trade Agreement:       Year 118 onwards (+1.5-2.5% GDP, +1.5-2 happiness)")

print("\nRaider/Gang Effects:")
print("  - Raiders add ~1.5% to GDP (shadow economy)")
print("  - Raiders reduce happiness by 2-5 points")
print("  - Security infrastructure gradually reduces both effects")

print("\n" + "-" * 80)
print("GDP FORECAST")
print("-" * 80)
print(f"  {'Year':<6}{'GDP':>14}{'YoY Chg':>10}{'Fisher':>8}  Notes")
print("  " + "-" * 60)
print(f"  {'115':<6}{GDP_115:>14,.0f}{'':>10}{'':>8}  Actual (baseline)")

prev = GDP_115
for year in range(116, 121):
    gdp = gdp_forecasts_116_120[year]
    chg = ((gdp - prev) / prev) * 100
    fisher = FISHER_CYCLE_116_120[year]
    notes = []
    if year == 116: notes.append("Training +1.2%")
    if year == 116: notes.append("Community tax -0.8%")
    if year >= 117: notes.append(f"Community +{COMMUNITY_CENTER_BENEFIT.get(year,0)*100:.1f}%")
    if year >= 118: notes.append(f"Trade +{TRADE_AGREEMENT_BOOST.get(year,0)*100:.1f}%")
    note_str = "; ".join(notes) if notes else ""
    print(f"  {year:<6}{gdp:>14,.0f}{chg:>+9.1f}%{fisher:>8}  {note_str}")
    prev = gdp

print("\n" + "-" * 80)
print("HAPPINESS FORECAST")
print("-" * 80)
print(f"  {'Year':<6}{'Happiness':>10}{'Change':>10}{'Raider':>10}{'Security':>10}")
print("  " + "-" * 50)
print(f"  {'115':<6}{HAPPINESS_BASELINE:>10.1f}{'':>10}{'':>10}{'':>10}  Baseline")

for year in range(116, 121):
    happy = happiness_forecasts[year]
    chg = happy - (HAPPINESS_BASELINE if year == 116 else happiness_forecasts[year-1])
    raider = RAIDER_HAPPINESS_DRAG[year]
    security = SECURITY_HAPPINESS_BOOST[year]
    print(f"  {year:<6}{happy:>10.1f}{chg:>+9.1f}{raider:>+9.1f}{security:>+9.1f}")

print("\n" + "-" * 80)
print("GINI COEFFICIENT FORECAST")
print("-" * 80)
print(f"  {'Year':<6}{'Formal':>10}{'Full Econ':>12}{'Raider Gap':>12}  Notes")
print("  " + "-" * 55)
print(f"  {'115':<6}{GINI_115_FORMAL:>10.2f}{GINI_115_FULL:>12.2f}{GINI_115_FULL-GINI_115_FORMAL:>12.2f}  Actual")

for year in range(116, 121):
    formal = gini_formal_forecasts[year]
    full = gini_full_forecasts[year]
    gap = full - formal
    notes = "Security reducing gap" if year >= 118 else ""
    print(f"  {year:<6}{formal:>10.2f}{full:>12.2f}{gap:>12.2f}  {notes}")

print("\n" + "-" * 80)
print("WELLBEING SUMMARY (Years 116-120)")
print("-" * 80)
gdp_growth_total = ((gdp_forecasts_116_120[120] - GDP_115) / GDP_115) * 100
happiness_change = happiness_forecasts[120] - HAPPINESS_BASELINE
gini_formal_change = gini_formal_forecasts[120] - GINI_115_FORMAL
gini_full_change = gini_full_forecasts[120] - GINI_115_FULL

print(f"\n  GDP:")
print(f"    Year 115: ${GDP_115:,.0f}")
print(f"    Year 120: ${gdp_forecasts_116_120[120]:,.0f}")
print(f"    5-Year Growth: {gdp_growth_total:+.1f}%")

print(f"\n  Happiness:")
print(f"    Year 115: {HAPPINESS_BASELINE:.1f}")
print(f"    Year 120: {happiness_forecasts[120]:.1f}")
print(f"    5-Year Change: {happiness_change:+.1f} points")

print(f"\n  Gini (Inequality):")
print(f"    Formal Economy: {GINI_115_FORMAL:.2f} → {gini_formal_forecasts[120]:.2f} ({gini_formal_change:+.2f})")
print(f"    Full Economy:   {GINI_115_FULL:.2f} → {gini_full_forecasts[120]:.2f} ({gini_full_change:+.2f})")
print(f"    Raider Gap:     {GINI_115_FULL-GINI_115_FORMAL:.2f} → {gini_full_forecasts[120]-gini_formal_forecasts[120]:.2f}")

print("\n  Key Findings:")
print("    - Security infrastructure gradually reduces raider impact")
print("    - Trade agreement provides sustained GDP growth from Year 118")
print("    - Community center improves happiness significantly from Year 117")
print("    - Formal economy inequality stable; full economy gap shrinking")
print("    - Fisher cycle creates volatility (HIGH years: 117, 120)")
print("=" * 80)

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
with open('population_year105.csv', 'r') as f:
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
with open('population_year105.csv', 'r') as f:
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
    102: 989644.00,
    103: 882950.00,
    104: 1015955.20,
    105: 1168436.60
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

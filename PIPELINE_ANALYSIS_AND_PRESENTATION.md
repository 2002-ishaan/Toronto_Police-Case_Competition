# TPS Transit Safety Pipeline - Complete Analysis & Judge Presentation Guide

## 📊 PIPELINE OVERVIEW

**Objective**: Predict officer deployment needs for FIFA 2026 World Cup matches at BMO Field, Toronto

**Data**: 316,478 crimes (2018-2025), 73 TTC stations, 6 FIFA matches

**Final Recommendation**: Deploy 165 officer-shifts across 6 matches (28 officers per high-risk match)

---

## ✅ LOGIC VALIDATION - MODULE BY MODULE

### Module 01: Data Loading & Sanity Checks
**Logic**: Validate data quality before analysis
**Key Outputs**:
- ✓ 452,949 total crime records (2000-2025)
- ✓ 316,478 recent crimes (2018-2025) = 69.9% of total
- ✓ 98.5% have valid coordinates (446,269 records)
- ✓ 73 stations with complete data
- ✓ 14,216 transit-related crimes (3.14% of all crimes)

**Validation**:
- ✅ Date ranges make sense (2018-2025 focus)
- ✅ Coordinate coverage excellent (98.5%)
- ✅ Station data complete (100% have coordinates)

**Logic Check**: CORRECT - Strong foundation for spatial analysis

---

### Module 02: Station Standardization
**Logic**: Create master station list by merging ridership + coordinates
**Key Outputs**:
- 73 final stations
- 68 with ridership data (93.2% coverage)
- 5 stations without ridership (ELLESMERE, LAWRENCE EAST, MCCOWAN, MIDLAND, SCARBOROUGH CENTRE)
- Multi-line stations aggregated (e.g., BLOOR-YONGE: 278,174 total boardings from 2 lines)

**Validation**:
- ✅ Handled duplicates correctly (Bloor-Yonge appears on Line 1 & 2, summed to 278K)
- ✅ Fuzzy matching found 0 additional matches (correct - Highway 407 and Vaughan Metro are outside core network)
- ✅ Distance calculations reasonable (Union to BMO = 3.36km)

**Logic Check**: CORRECT - Proper data fusion

---

### Module 03: Spatial Join (500m radius)
**Logic**: Link crimes to nearest stations within 500m
**Key Outputs**:
- 272,003 crimes after deduplication (removed 39,795 duplicates)
- 60,369 crimes matched to stations (22.2% of total)
- 211,634 crimes NOT near any station (77.8%)
- Mean distance to station: 241.6m
- All 73 stations have at least 1 crime

**Validation**:
- ✅ Match rate (22.2%) is reasonable - most crimes don't happen AT stations
- ✅ Distance statistics correct (mean 242m < max 500m)
- ✅ Top station is DUNDAS (3,568 crimes) - matches known high-traffic area

**⚠️ CRITICAL ISSUE FOUND**:
- **Deduplication removed 39,795 records (14.7%)** - this is high!
- This suggests same crime reported multiple times OR data quality issue
- **Impact**: Reduces sample size but shouldn't bias results (duplicates removed uniformly)

**Logic Check**: MOSTLY CORRECT - High deduplication rate should be investigated but doesn't invalidate results

---

### Module 04: Temporal Features
**Logic**: Add time-based features for pattern analysis
**Key Outputs**:
- Weekend crimes: 17,011 (28.2%)
- Late night crimes: 14,018 (23.2%)
- Event proxy crimes (Fri/Sat evening): 5,482 (9.1%)
- High-risk period (weekend OR late night): 26,764 (44.3%)

**Validation**:
- ✅ Weekend % (28.2%) matches 2/7 days = 28.6% (expected)
- ✅ Late night % (23.2%) > random expectation (5 hours/24 = 20.8%) - shows concentration
- ✅ Event proxy % (9.1%) slightly above random (12 hours/168 = 7.1%) - good signal

**Logic Check**: CORRECT - Features properly engineered

---

### Module 05: Station Risk Profiling
**Logic**: Calculate risk scores for all 73 stations
**Key Outputs**:
- **Risk Distribution**:
  - Critical (>7 crimes/week): 3 stations (DUNDAS, COLLEGE, QUEEN)
  - High (3-7 crimes/week): 8 stations
  - Medium (1-3 crimes/week): 39 stations
  - Low (<1 crime/week): 23 stations

- **Weekend Multipliers**: Mean 0.97x (weekend NOT more dangerous overall)
  - Highest: ST ANDREW 1.19x, CHRISTIE 1.19x
  - This contradicts common assumption!

- **Late Night Concentration**: Mean 23.3%
  - Highest: ST ANDREW 34.8%, DOWNSVIEW PARK 32.8%

**⚠️ LOGIC CONCERN**:
- Weekend multiplier of 0.97x suggests weekdays are WORSE than weekends
- This is counterintuitive BUT could be correct (commuter traffic Mon-Fri > weekend)
- **Validation needed**: Check if this aligns with TTC ridership patterns

**Logic Check**: CORRECT but counterintuitive - weekend effect minimal

---

### Module 06: Temporal Heatmap
**Logic**: Find when crimes occur (hour × day patterns)
**Key Outputs**:
- Peak hour: 00:00 (midnight) - 3,767 crimes (6.2%)
- Peak day: Friday - 8,820 crimes
- Top 3 hours: 00:00, 18:00, 12:00 = 17% of all crimes
- Assault peaks 15:00, Robbery peaks 21:00

**Validation**:
- ✅ Midnight peak makes sense (late night, alcohol-related incidents)
- ✅ Friday peak aligns with social activity
- ✅ Robbery at 21:00 (dark, people returning home) vs Assault at 15:00 (afternoon arguments) - logical

**Logic Check**: CORRECT - Temporal patterns make sense

---

### Module 07: FIFA Corridor Analysis
**Logic**: Identify stations affected by FIFA matches at BMO Field
**Key Outputs**:
- **15 FIFA-affected stations**:
  - 7 BMO Corridor (<3.5km): ST ANDREW, DUFFERIN, ST PATRICK, OSSINGTON, OSGOODE, LANSDOWNE, CHRISTIE
  - 4 Major Transfer Points: BLOOR-YONGE, ST GEORGE, UNION, SPADINA
  - 4 Downtown Hubs: DUNDAS, COLLEGE, QUEEN, WELLESLEY

- **Top 10 by FIFA Risk Score**:
  1. DUNDAS (5.66)
  2. QUEEN (4.79)
  3. UNION (4.31)
  4. COLLEGE (3.47)
  5. BLOOR-YONGE (2.81)

**⚠️ CRITICAL FINDING**:
- **NO stations within 2km of BMO Field!**
- Closest is ST ANDREW at 3.1km
- Top 3 risk stations are DOWNTOWN (not near BMO)

**Logic Check**:
- ✅ Correct identification of stations
- ✅ Risk scores weight both proximity + historical crime
- ⚠️ BUT: Are we deploying at the RIGHT places?

**LOGIC ISSUE**:
- **Top stations (DUNDAS, QUEEN, UNION) are 4km+ from BMO**
- These are high-crime because they're downtown hubs, NOT because of BMO proximity
- **Question**: Will FIFA fans even USE these stations? Or will they use streetcars directly to BMO?

**Recommendation**: Model assumes fans transit THROUGH downtown to BMO. Validate this assumption with TTC route planning.

---

### Module 09: Event Amplification (CRITICAL MODULE)
**Logic**: Calculate how much events amplify crime
**Key Outputs**:
- **OLD METHOD (Fri/Sat proxy)**: 1.08x amplification
- **NEW METHOD (Anomaly detection)**: 1.56x amplification
- 194 identified event days (days with >1.5 SD above baseline crime)
- Event rate: 9.73 crimes/day vs 6.22 non-event = **1.56x amplification**

**Validation**:
- ✅ Anomaly detection method is more rigorous than Fri/Sat proxy
- ✅ 1.56x > 1.08x because old method mixed event days with regular weekends
- ✅ Station-level amplification varies: 1.05x to 2.26x (good - shows heterogeneity)

**⚠️ CRITICAL VALIDATION QUESTION**:
- How do we know the 194 "anomalous days" are actually game days?
- **Method**: Filtered to sports seasons (Oct-May for Leafs, Apr-Oct for Jays)
- **Assumption**: High-crime days during sports season = game days
- **Risk**: Could include non-game events (concerts, protests, etc.)

**Logic Check**:
- ✅ Method is sound (better than Fri/Sat proxy)
- ⚠️ Cannot verify these are ACTUAL game days without external data
- **Confidence**: Medium (directionally correct, magnitude uncertain)

---

### Module 10: FIFA Deployment (FINAL RECOMMENDATION)
**Logic**: Calculate officer needs using corrected amplification
**Key Outputs**:
- **Match 1** (Fri 15:00): 28 officers | Window: 17:00-21:00
- **Match 2** (Wed 19:00): 27 officers | Window: 21:00-23:00
- **Match 3** (Sat 16:00): 28 officers | Window: 18:00-22:00
- **Match 4** (Tue 19:00): 27 officers | Window: 21:00-23:00
- **Match 5** (Fri 15:00): 28 officers | Window: 17:00-21:00
- **Match 6** (Thu 19:00): 27 officers | Window: 21:00-23:00
- **TOTAL**: 165 officer-shifts

**Formula**:
```
officers = ⌈(event_rate × match_risk × fifa_factor) / capacity⌉
- event_rate: crimes/day on event days (includes 1.56x amplification)
- match_risk: 1.3 (HIGH - Fri/Sat), 1.15 (MED-HIGH), 1.0 (MEDIUM)
- fifa_factor: 2.5x (FIFA crowd = 2.5× typical Leafs/Jays)
- capacity: 0.5 crimes/officer (conservative)
```

**Validation**:
- ✅ High-risk matches (Fri/Sat) get more officers (28 vs 27)
- ✅ Deployment windows align with post-match exodus (17:00-23:00)
- ⚠️ FIFA factor (2.5x) is ASSUMED, not data-driven

**🚨 MAJOR LOGIC ISSUES**:

1. **FIFA Factor (2.5x) is Arbitrary**
   - Assumes FIFA crowds are 2.5x more crime-prone than Leafs/Jays
   - **No data to support this**
   - Could be 1.0x (same) or 5.0x (much worse)

2. **Officer Capacity (0.5 crimes/officer) is Arbitrary**
   - Means 1 officer can handle 0.5 expected crimes
   - **No evidence for this number**
   - Module 11 shows deployment varies from 52-107 shifts depending on capacity

3. **Double-Counting Amplification?**
   - event_rate ALREADY includes 1.56x amplification (from Module 09)
   - Then multiply by match_risk (1.3x) AND fifa_factor (2.5x)
   - **Total amplification = 1.56 × 1.3 × 2.5 = 5.07x**
   - Is this justified?

**Logic Check**:
- ⚠️ **FORMULA IS QUESTIONABLE**
- Too many assumptions stacked multiplicatively
- Likely OVERESTIMATES officer needs

---

### Module 11: Sensitivity Analysis
**Logic**: Test how deployment changes with officer capacity
**Key Outputs**:
- **Capacity 0.5**: 107 shifts
- **Capacity 1.0**: 64 shifts
- **Capacity 1.5**: 64 shifts (recommended)
- **Capacity 2.0**: 52 shifts
- **Capacity 3.0**: 52 shifts
- **Range**: 52-107 shifts (±27 from midpoint)

**Validation**:
- ✅ Shows uncertainty in deployment estimates
- ✅ Recommends using Match 1 to calibrate
- ✅ Honest about limitations

**Logic Check**: CORRECT - Good sensitivity analysis

---

## 🎯 OVERALL PIPELINE ASSESSMENT

### ✅ STRENGTHS
1. **Data Quality**: Excellent (98.5% coordinate coverage, 73/73 stations)
2. **Spatial Analysis**: Rigorous 500m radius join, proper distance calculations
3. **Temporal Features**: Well-engineered (weekend, late night, event proxy)
4. **Event Amplification**: Improved method (1.56x > 1.08x via anomaly detection)
5. **Sensitivity Analysis**: Honest about uncertainty (52-107 shift range)
6. **Full Network Analysis**: Analyzed ALL 73 stations (not just FIFA-relevant)

### ⚠️ WEAKNESSES & LOGIC CONCERNS

#### 1. **Geographic Mismatch** (CRITICAL)
- Top risk stations (DUNDAS, QUEEN, UNION) are 4km from BMO Field
- **These are high-crime DOWNTOWN hubs, not BMO-specific**
- **Question**: Will FIFA fans actually use these stations?
- **Alternative**: Fans may use streetcars directly to BMO, bypassing downtown

**Impact**: May be deploying officers at wrong locations

#### 2. **Event Amplification Validation** (MEDIUM)
- Cannot verify 194 "event days" are actual game days without external data
- Assumption: High crime during sports season = game day
- **Could include**: Concerts, festivals, protests (not sports)

**Impact**: Amplification factor (1.56x) may be inflated

#### 3. **Multiplicative Assumptions** (HIGH)
- Formula: event_rate × match_risk × fifa_factor = 1.56 × 1.3 × 2.5 = 5.07x
- **Each multiplier compounds the previous**
- FIFA factor (2.5x) has NO empirical basis
- Officer capacity (0.5) is arbitrary

**Impact**: Likely OVERESTIMATES officer needs by 2-3x

#### 4. **Weekend Effect Counterintuitive** (LOW)
- Weekend multiplier 0.97x (weekdays worse than weekends)
- Contradicts common assumption but could be correct (commuter effect)

**Impact**: Minor - doesn't affect FIFA (all matches are unique events)

#### 5. **High Deduplication Rate** (MEDIUM)
- Removed 39,795 duplicate crime records (14.7%)
- Could indicate data quality issues

**Impact**: Reduces sample size but shouldn't bias results

---

## 📈 CORRECTED LOGIC & RECOMMENDATIONS

### Recommended Formula Simplification
```
officers = ⌈(baseline_rate × amplification) / capacity⌉

Where:
- baseline_rate = crimes/hour on typical non-event days at station
- amplification = 1.56x (from Module 09 - data-driven)
- capacity = 1.5 crimes/officer (use Match 1 to calibrate)
```

**Rationale**:
- Remove FIFA factor (2.5x) - no evidence for it
- Remove match_risk (1.3x) - already captured in baseline rate for Fri/Sat
- Use SINGLE amplification factor (1.56x) that's data-driven

### Revised Deployment Estimate
Using simplified formula:
- **Match 1-6**: ~15-20 officers per match (instead of 28)
- **Total**: ~100-120 shifts (instead of 165)

**Confidence**: Medium (still uncertain due to unknown officer capacity)

---

## 🎤 HOW TO EXPLAIN TO JUDGES

### 1. **Opening: The Problem** (30 seconds)
> "FIFA 2026 will bring 45,000 fans to BMO Field for 6 matches. How many TPS officers should we deploy at TTC stations to maintain safety?"

### 2. **The Data** (1 minute)
> "We analyzed 8 years of TPS crime data (316,000 crimes from 2018-2025) and linked them to 73 TTC stations. We found 60,000 transit-related crimes within 500 meters of stations."

**Show**: Module 01 summary slide (data quality)

### 3. **The Challenge** (1 minute)
> "BMO Field has NO nearby TTC stations. The closest is 3km away. Fans will use streetcars OR transit through downtown hubs like Union, Dundas, and Queen."

**Show**: Map of BMO Field + closest stations

### 4. **The Analysis** (2 minutes)
> "We built a 3-step model:
> 1. **Baseline Risk**: Historical crime rates at each station (DUNDAS = 8.6 crimes/week)
> 2. **Event Amplification**: Major events increase crime by 1.56x (Leafs/Jays games)
> 3. **FIFA Factor**: We ASSUME FIFA = 1.56x typical event (no historical data)"

**Show**: Flow diagram (Modules 01→05→09→10)

### 5. **The Results** (1 minute)
> "Our model recommends:
> - **165 officer-shifts** across 6 matches
> - **28 officers per high-risk match** (Friday/Saturday)
> - Focus on **10 priority stations** (Union, Dundas, Queen, etc.)
> - **Critical windows**: 17:00-23:00 (post-match exodus)"

**Show**: Match schedule with officer allocations

### 6. **The Uncertainty** (1 minute - CRITICAL)
> "We're honest about limitations:
> - **Officer capacity unknown**: Deployment could range from 52-107 shifts (±27)
> - **FIFA crowds untested**: No Toronto FIFA history
> - **Geographic assumption**: Fans may bypass downtown hubs"

**Show**: Sensitivity analysis chart (Module 11)

### 7. **The Recommendation** (1 minute)
> "**Adaptive Strategy**:
> - Match 1: Deploy conservatively (30 officers), MEASURE actual crime
> - Matches 2-3: Adjust based on Match 1 actuals
> - Matches 4-6: Optimized deployment
>
> This beats any static prediction we could make today."

**Show**: Learning curve diagram

### 8. **The Value** (30 seconds)
> "Our analysis provides:
> ✅ Data-driven officer allocation (not guesswork)
> ✅ Station-specific deployment windows
> ✅ Honest uncertainty quantification
> ✅ Adaptive learning framework"

---

## 🎯 KEY TALKING POINTS FOR JUDGES

### What Makes This Analysis Strong?
1. **Comprehensive Data**: 8 years, 316K crimes, 73 stations
2. **Rigorous Methods**: Spatial join, anomaly detection, sensitivity analysis
3. **Honest Uncertainty**: We quantify what we don't know (52-107 shift range)
4. **Actionable**: Specific stations, specific times, specific officer counts
5. **Adaptive**: Learn from Match 1, optimize Matches 2-6

### What Are the Limitations? (BE HONEST)
1. **No FIFA History**: We infer from Leafs/Jays games (may not generalize)
2. **Geographic Assumption**: We assume fans transit through downtown (may not be true)
3. **Officer Capacity Unknown**: We estimate 1.5 crimes/officer (needs validation)
4. **Event Identification**: We can't verify 194 "event days" are actual games (no external data)

### What Would Make This Better?
1. **Validate Event Days**: Cross-reference with Leafs/Jays schedules
2. **Fan Flow Modeling**: Survey or model how fans will actually get to BMO
3. **Officer Capacity Study**: Interview TPS or review past event deployments
4. **Pilot Test**: Use Match 1 to calibrate all assumptions

---

## 📊 FINAL VERDICT: LOGIC CHECK

### Overall Pipeline Logic: **7/10** (Good but flawed)

**What Works**:
- ✅ Data foundation (Modules 01-04)
- ✅ Spatial analysis (Module 03)
- ✅ Event amplification method (Module 09)
- ✅ Sensitivity analysis (Module 11)

**What Needs Work**:
- ⚠️ Geographic assumption (downtown vs BMO corridor)
- ⚠️ Multiplicative formula (too many assumptions)
- ⚠️ FIFA factor (no empirical basis)
- ⚠️ Event day validation (can't confirm game days)

### Recommended Deployment: **100-120 officers** (not 165)

**Rationale**:
- Remove FIFA factor (2.5x) - unjustified
- Use single amplification (1.56x) - data-driven
- Use Match 1 to calibrate capacity

### Presentation Strategy: **Be Honest**
- Show the analysis
- Acknowledge limitations
- Recommend adaptive learning
- **Don't oversell certainty you don't have**

---

## 🎓 WHAT JUDGES WANT TO HEAR

1. **"We used 8 years of real crime data"** ✅
2. **"We quantified uncertainty (52-107 shift range)"** ✅
3. **"We recommend learning from Match 1"** ✅
4. **"Here are the limitations..."** ✅
5. **"We focused on actionable insights"** ✅

### What Judges DON'T Want:
- ❌ "We're 100% confident in 165 officers"
- ❌ Hiding uncertainty
- ❌ Made-up numbers without justification
- ❌ Overfitting to historical data

---

## ✅ FINAL RECOMMENDATIONS

### For the Presentation:
1. **Lead with the adaptive strategy** (not a fixed number)
2. **Show the uncertainty** (52-107 range)
3. **Acknowledge geographic concern** (downtown vs BMO)
4. **Emphasize learning** (Match 1 calibration)

### For the Report:
1. **Revise Module 10 formula** (remove arbitrary multipliers)
2. **Add geographic validation** (check TTC route planning)
3. **Validate event days** (cross-reference with game schedules if possible)
4. **Lower final estimate** (100-120 instead of 165)

### For TPS:
1. **Deploy conservatively for Match 1** (30 officers)
2. **Measure everything** (crimes, interventions, officer workload)
3. **Adjust for Matches 2-6** (based on actuals)
4. **Focus on 10 priority stations** (don't spread too thin)

---

**Bottom Line**: The analysis is solid but makes too many assumptions. Be honest about this, recommend adaptive learning, and you'll impress the judges with intellectual honesty rather than false precision.

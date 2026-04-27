## Data Preparation
### Passenger Dataset `TIPOLOGIA_VIAGGIATORE`

Several preprocessing steps were applied to ensure consistency and data quality:

- Standardized inconsistent categorical columns (e.g., nationality, document type, airline)
- Converted `DATA_PARTENZA` into a proper datetime format
- Standardized country codes to 3-letter ISO format
- Replaced placeholder values (e.g., `N.D.`) with null values
- Removed duplicate rows
- Standardized airport codes (uppercase formatting)

Logical constraints were enforced:
- `ENTRATI ≥ INVESTIGATI ≥ ALLARMATI`

Violations were corrected using rule-based adjustments. Rows that remained inconsistent were removed.

Additionally:
- Extreme outliers in `ENTRATI` were removed using a conservative upper bound based on realistic aircraft capacity

---

### Cases Dataset `ALLARMI`

The cases dataset was cleaned with similar principles:

- Removed redundant or low-information columns
- Standardized `DATA_PARTENZA`
- Cleaned and standardized `tot voli`
- Removed duplicate rows
- Replaced placeholder values (`???`, `N/C`, etc.) with `UNKNOWN`
- Standardized categorical values (countries, zones, airport descriptions)
- Fixed logical inconsistencies in region assignments

All columns were translated into English for consistency.

---

## Feature Engineering

### Analytical Grain

The dataset is aggregated at:

**`date × route_airport`**

This grain was selected because:
- it guarantees uniqueness
- it aligns best with operational behavior
- it provides the most precise level for anomaly detection

`route_city` and `route_country` are retained for interpretability.

---

### Base Features

Core operational features:

- `entries`
- `investigated`
- `flagged`
- `investigation_rate`
- `flag_rate`
- `flag_given_investigated`

These capture:
- passenger volume
- control intensity
- flagged outcomes

---

### Calendar Features

Derived from date:

- `year`, `month`, `day`
- `weekday`
- `is_weekend`

These enable detection of:
- temporal patterns
- weekday/weekend effects
- periodic trends

---

### Segment-Level Features

Aggregated features were created for:

- nationality
- document type
- airline
- control result

For each segment, we compute:

- count (diversity)
- average values
- maximum values
- average and maximum flag rates

This captures:
- passenger heterogeneity
- concentration effects
- segment-level behavioral patterns

---

### Case-Based Features

Cases data was aggregated and merged using:

**`date + route_airport`**

Features include:

- `has_case_match`
- `case_records`
- `total_flights`
- `unique_alarm_reasons`
- `unique_event_types`
- `alarm_density_per_entry`

Important:

- `has_case_match` is created before filling missing values
- unmatched rows are explicitly preserved
- case features are treated as contextual signals

Case coverage:
- ~34.6% of rows have matching case data

---

### Temporal Change Features

Time-based features were created per `route_airport`:

- `lag1` → previous value
- `diff1` → absolute change
- `pct_change1` → relative change

Applied to:

- `entries`
- `investigated`
- `flagged`
- `investigation_rate`
- `flag_rate`

These capture:
- trend changes
- sudden increases/decreases
- behavioral shifts

Note:
- Missing values are expected when no previous observation exists
- `pct_change` is undefined when the previous value is zero

---

### Low-Volume Indicators

Due to strong skewness in traffic:

- ~70% of rows have fewer than 10 entries

Two features were added:

- `is_low_volume`
- `is_low_volume_50`

These preserve information without discarding low-volume observations.

---
Some features were excluded due to:

- high sparsity
- instability (e.g., division by zero issues)

Examples:
- `alarm_density_per_flight`
- some percentage-change variables

The final output provides:

- operational activity signals
- behavioral indicators
- temporal dynamics
- contextual case information

---

## Data Preparation

After feature engineering, two types of historical baselines were added to capture what "normal" looks like for each route:

### Rolling Averages

Observation-based windows (not calendar-based) were computed per `route_airport` over:

- `entries`, `flag_rate`, `investigation_rate`

For each metric, three columns were created:

- 7-observation rolling mean (`min_periods=3`)
- 30-observation rolling mean (`min_periods=7`)
- Deviation ratio: current value divided by 7-obs rolling mean

Why observation-based windows: the dataset is irregular (median 3-day gap between consecutive observations on the same route, some routes with month-long gaps). A calendar-based 7-day window would often contain only 1-2 data points, making the average unreliable.

### Monthly Seasonal Baselines

Standard `seasonal_decompose` requires regularly-spaced daily data, which our dataset doesn't provide. We replaced it with a monthly baseline: for each `route_airport × month`, the average entries are computed and used as a reference. Two derived columns capture deviation:

- `entries_residual` — absolute deviation from the monthly baseline
- `entries_residual_z` — z-score normalized per route

A static route-level mean (`entries_route_mean`) is also added as a stable reference, especially useful for routes with too few observations to support rolling windows.

### Missing Value Handling

A column-group-specific strategy was applied:

- `lag/diff/pct_change` columns: filled with 0 (first observation per route has no previous value)
- `flag_given_investigated`: filled with 0 (undefined when `investigated = 0`)
- Rate columns: filled with 0 (undefined when `entries = 0`)
- Rolling features: filled with column median (routes with too few observations)
- Seasonal features: filled with 0 (single-observation months produce undefined std)

---

## Anomaly Detection

Three complementary unsupervised methods were applied with `contamination=0.05`:

- **Isolation Forest** — global outliers in high-dimensional space
- **Local Outlier Factor** — local density anomalies
- **Multivariate Z-score** — extreme single-feature outliers

A consensus flag was built through majority voting: an observation is flagged when at least 2 out of 3 methods agree. Fixing `contamination=0.05` ensures comparable detection rates across methods, isolating the value of consensus to *which* rows each model flags rather than how many.

Feature importance was extracted from the Isolation Forest. The deviation ratios, monthly z-score and route mean dominate the ranking — confirming that the Data Preparation step drives most of the detection.

---

## Post-Processing

Four business rules were applied on top of the model output:

- `flag_rate_dev_ratio7 > 3` — flag rate exceeded 3× recent baseline
- `entries_dev_ratio7 > 3` — passenger volume exceeded 3× recent baseline
- `abs(entries_residual_z) > 2` — entries deviate more than 2σ from the monthly norm
- `alarm_density_per_entry > 95th percentile` — disproportionate alarm cases

The final anomaly label combines model consensus and business rules:

final_anomaly = consensus_anomaly OR rule_any

This captures both statistically unusual observations and operationally meaningful patterns. Out of 3,449 observations, 487 (14.1%) were flagged — 75 by model consensus, 430 by rules, with 18 overlapping.
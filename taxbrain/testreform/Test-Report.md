% Test Report
% 
% July 7, 2025

## Table of Contents

### [Introduction](#Introduction)
* [Analysis Summary](#Summary)
* [Notable Changes](#Notable-Changes)

### [Aggregate Changes](#Aggregate-Changes)
### [Distributional Analysis](#Distributional-Analysis)
### [Summary of Policy Changes](#Summary-of-Policy-Changes)
### [Baseline Policy](#Policy-Baseline)
### [Assumptions](#Assumptions)
* [Behavioral Assumptions](#Behavioral-Assumptions)
* [Consumption Assumptions](#Consumption-Assumptions)
* [Growth Assumptions](#Growth-Assumptions)

### [Citations](#citations)

\vfill
![](/Users/max/Code/Tax-Calculator-thru74/taxbrain/report_files/taxbrain.png){.center}

\pagebreak

## Introduction

This report summarizes the fiscal impact of modifing the payroll taxes, standard deduction, and Social Security taxability sections of the tax code. The baseline for this analysis is current law as of July 7, 2025.

## Summary

Over the budget window  (2018 to 2019), this policy is expected to increase aggregate tax liability by $5.7 trillion. Those with expanded income less than $0K are expected to see the largest change in tax liability. On average, this group can expect to see their tax liability remain the same.



## Notable Changes


No notable variables changed by more than 5.00%


## Aggregate Changes

**Table 1: Total Tax Liability (Billions)**

|            | 2018    | 2019    | Total   |
|:-----------|:--------|:--------|:--------|
| Base       | 250,255 | 260,752 | 511,008 |
| Reform     | 250,255 | 263,588 | 513,843 |
| Difference | 0       | 2,835   | 2,835   |

**Table 2: Total Tax Liability Change by Tax Type (Billions)**

|             |   2018 |   2019 |   Total |
|:------------|-------:|-------:|--------:|
| Income Tax  |      0 |    -28 |     -28 |
| Payroll Tax |      0 |     60 |      60 |
| Combined    |      0 |     31 |      31 |

![Change in Aggregate Tax Liability](testreform/difference_graph.png)
\ 

## Distributional Analysis

**Table 3: Differences Table - 2018**^[The _0-10n_ bin is comprised of tax units with negative income, the _0-10z_ bin is comprised of tax units with no income, and the _0-10p_ bin is comprised of tax units in the bottom decile with positive income.]

| _Income &nbsp; Decile_   |   Number of Returns |   Percent with Tax Cut |   Percent with Tax Increase |   Average Tax Change |   Total Tax Difference |   Universal Basic Income |   Total Cost of Benefits |   Consumption Value of Benefits |   % Change in After-Tax Income |
|:-------------------------|--------------------:|-----------------------:|----------------------------:|---------------------:|-----------------------:|-------------------------:|-------------------------:|--------------------------------:|-------------------------------:|
| 0-10n                    |                 8.1 |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 0-10z                    |                12   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 0-10p                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 10-20                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 20-30                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 30-40                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 40-50                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 50-60                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 60-70                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 70-80                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 80-90                    |                20   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 90-100                   |               200   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| ALL                      |                10   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 90-95                    |                 8   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| 95-99                    |                 2   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |
| Top 1%                   |               200   |                      0 |                           0 |                    0 |                      0 |                        0 |                        0 |                               0 |                              0 |



![Percentage Change in After Tax Income](testreform/dist_graph.png)
\ 

## Summary of Policy Changes


_2019_

| Policy                                                                         | Original Value    | New Value          |
|:-------------------------------------------------------------------------------|:------------------|:-------------------|
| Threshold for Social Security benefit taxability 1 - Single                    | 25,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 1 - Married Filing Jointly    | 32,000.0          | 100,000            |
| Threshold for Social Security benefit taxability 1 - Married Filing Separately | 25,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 1 - Head of Household         | 25,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 1 - Widow                     | 25,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 2 - Single                    | 34,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 2 - Married Filing Jointly    | 44,000.0          | 100,000            |
| Threshold for Social Security benefit taxability 2 - Married Filing Separately | 34,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 2 - Head of Household         | 34,000.0          | 50,000             |
| Threshold for Social Security benefit taxability 2 - Widow                     | 34,000.0          | 50,000             |
| Additional Taxable Earnings Threshold for Social Security                      | 9e+99             | 400,000            |
| Standard deduction amount                                                      | CPI Indexed: True | CPI Indexed: False |

_2020_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |      0.0625 |

_2021_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |       0.063 |

_2022_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |      0.0635 |

_2023_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |       0.064 |

_2024_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |      0.0645 |

_2025_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |       0.065 |

_2026_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |      0.0605 |

_2027_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |       0.061 |

_2028_

| Policy                                         |   Original Value |   New Value |
|:-----------------------------------------------|-----------------:|------------:|
| Employee side Social Security payroll tax rate |            0.062 |      0.0615 |


## Policy Baseline

This report is based on current law as of July 7, 2025.

## Assumptions

### Behavioral Assumptions


* No behavioral assumptions


### Consumption Assumptions




No new consumption assumptions specified.


### Growth Assumptions




No new growth assumptions specified.


## Citations

This analysis was conducted using the following open source economic models:


* Tax-Brain release 1.0.0

* Tax-Calculator release 4.6.3a

* Behavioral-Responses release 0.0.0

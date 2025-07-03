import pandas as pd
from collections import defaultdict
from taxbrain.utils import weighted_sum
from taxcalc.utils import (
    create_distribution_table,
    create_difference_table,
)

def weighted_totals(
    var: str, base_records, reform_records, base_data, reform_data, start_year, end_year, base_calc, reform_calc, include_total: bool = False, xtot: int = 0
) -> pd.DataFrame:
    """
    Create a pandas DataFrame that shows the weighted sum or a specified
    variable under the baseline policy, reform policy, and the difference
    between the two.

    Parameters
    ----------
    var: str
        Variable name for variable you want the weighted total of.
    include_total: bool
        If true the returned DataFrame will include a "total" columns

    Returns
    -------"""
    base_totals = {}
    reform_totals = {}
    differences = {}
    for year in range(start_year, end_year + 1):
        if xtot == 0:
            base_totals[year] = (
                getattr(base_records, 'WT')['WT2026'] * base_data[year][var]
            ).sum()
            reform_totals[year] = (
                getattr(reform_records, 'WT')['WT2026'] * reform_data[year][var]
            ).sum()
            differences[year] = reform_totals[year] - base_totals[year]
        else:
            base_data_full = pd.concat([base_calc, getattr(base_records, 'WT')], axis=1)
            base_data_filtered = base_data_full[base_data_full['XTOT']==xtot]
            base_totals[year] = (
                base_data_filtered["WT2026"] * base_data_filtered[var]
            ).sum()
            reform_data_full = pd.concat([reform_calc, getattr(reform_records, 'WT')], axis=1)
            reform_data_filtered = reform_data_full[reform_data_full['XTOT']==xtot]                
            reform_totals[year] = (
                reform_data_filtered["WT2026"] * reform_data_filtered[var]
            ).sum()
            differences[year] = reform_totals[year] - base_totals[year]


    table = pd.DataFrame(
        [base_totals, reform_totals, differences],
        index=["Base", "Reform", "Difference"],
    )
    if include_total:
        table["Total"] = table.sum(axis=1)
    return table

def multi_var_table(
    varlist: list, calc: str, start_year: int, end_year: int, base_data: dict, reform_data: dict, include_total: bool = False
) -> pd.DataFrame:
    """
    Create a Pandas DataFrame with multiple variables from the
    specified data source

    Parameters
    ----------
    varlist: list
        list of variables to include in the table
    calc: str
        specify reform or base calculator data, can take either
        `'REFORM'` or `'BASE'`
    include_total: bool
        If true the returned DataFrame will include a "total" column

    Returns
    -------"""
    if not isinstance(varlist, list):
        msg = f"'varlist' is of type {type(varlist)}. Must be a list."
        raise TypeError(msg)
    if calc.upper() == "REFORM":
        data = reform_data
    elif calc.upper() == "BASE":
        data = base_data
    else:
        raise ValueError("'calc' must be 'base' or 'reform'")
    data_dict = defaultdict(list)
    for year in range(start_year, end_year + 1):
        for var in varlist:
            data_dict[var] += [weighted_sum(data[year], var)]
    df = pd.DataFrame(
        data_dict, index=range(start_year, end_year + 1)
    )
    table = df.transpose()
    if include_total:
        table["Total"] = table.sum(axis=1)
    return table

def distribution_table(
    year: int,
    groupby: str,
    income_measure: str,
    calc: str,
    base_data: dict,
    reform_data: dict,
    pop_quantiles: bool = False,
) -> pd.DataFrame:
    """
    Method to create a distribution table

    Parameters
    ----------
    year: int
        which year the distribution table data should be from
    groupby: str
        determines how the rows in the table are sorted
        options: 'weighted_deciles', 'standard_income_bins',
        'soi_agi_bin'
    income_measure: str
        determines which variable is used to sort the rows in
        the table
        options: 'expanded_income' or 'expanded_income_baseline'
    calc: str
        which calculator to use, can take either
        `'REFORM'` or `'BASE'`
    calc: which calculator to use: base or reform
    pop_quantiles: bool
        whether or not weighted_deciles contain equal number of
        tax units (False) or people (True)

    Returns
    -------"""
    # pull desired data
    if calc.lower() == "base":
        data = base_data[year]
    elif calc.lower() == "reform":
        data = reform_data[year]
    else:
        raise ValueError("calc must be either BASE or REFORM")
    # minor data preparation before calling the function
    if pop_quantiles:
        data["count"] = data["s006"] * data["XTOT"]
    else:
        data["count"] = data["s006"]
    data["count_ItemDed"] = data["count"].where(data["c04470"] > 0.0, 0.0)
    data["count_StandardDed"] = data["count"].where(
        data["standard"] > 0.0, 0.0
    )
    data["count_AMT"] = data["count"].where(data["c09600"] > 0.0, 0.0)
    if income_measure == "expanded_income_baseline":
        base_income = base_data[year]["expanded_income"]
        data["expanded_income_baseline"] = base_income
    table = create_distribution_table(
        data, groupby, income_measure, pop_quantiles
    )
    return table

def differences_table(
    year: int,
    groupby: str,
    tax_to_diff: str,
    base_data: dict,
    reform_data: dict,
    pop_quantiles: bool = False,
) -> pd.DataFrame:
    """
    Method to create a differences table

    Parameters
    ----------
    year: int
        which year the difference table should be from
    groupby: str
        determines how the rows in the table are sorted
        options: 'weighted_deciles', 'standard_income_bins', 'soi_agi_bin'
    tax_to_diff: str
        which tax to take the difference of
        options: 'iitax', 'payrolltax', 'combined'
    pop_quantiles: bool
        whether weighted_deciles contain an equal number of tax
        units (False) or people (True)

    Returns
    -------
    table: Pandas DataFrame
        differences table
    """
    base_data = base_data[year]
    reform_data = reform_data[year]
    table = create_difference_table(
        base_data, reform_data, groupby, tax_to_diff, pop_quantiles
    )
    return table

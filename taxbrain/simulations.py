import taxcalc as tc
import behresp
from taxbrain.corporate_incidence import distribute as dist_corp


def taxcalc_advance(calc, varlist, year, corp_revenue, start_year, ci_params, reform=False):
    """
    This function advances the year used in Tax-Calculator, computes
    tax liability and rates, and saves the results to a dictionary.
    Args:
        calc (Tax-Calculator Calculator object): TC calculator
        varlist (list): variables to return
        year (int): year to begin advancing from
        reform (bool): whether Calculator object is for the reform policy

    Returns:
        tax_dict (dict): a dictionary of microdata with marginal tax
            rates and other information computed in TC
    """
    calc.advance_to_year(year)
    if corp_revenue is not None:
        if reform:
            calc = dist_corp(
                calc,
                corp_revenue,
                year,
                start_year,
                ci_params,
            )
    calc.calc_all()
    df = calc.dataframe(varlist)
    return df


def behresp_advance(base_calc, reform_calc, varlist, year, corp_revenue, start_year, ci_params, behavior_params):
    """
    This function advances the year used in the Behavioral Responses
    model and saves the results to a dictionary.
    Args:
        calc1 (Tax-Calculator Calculator object): TC calculator
        year (int): year to begin advancing from
    Returns:
        tax_dict (dict): a dictionary of microdata with marginal tax
            rates and other information computed in TC
    """
    base_calc.advance_to_year(year)
    reform_calc.advance_to_year(year)
    if corp_revenue is not None:
        reform_calc = dist_corp(
            reform_calc,
            corp_revenue,
            year,
            start_year,
            ci_params,
        )
    base, reform = behresp.response(
        base_calc, reform_calc, behavior_params, dump=True
    )
    base_df = base[varlist]
    reform_df = reform[varlist]
    return [base_df, reform_df]

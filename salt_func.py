import pandas as pd
from taxbrain.taxbrain import TaxBrain

def calc_rev_diff(single_amount, sub, cg):
    tcja_ext = "github://OFRA-ORG:Tax-Calculator-thru74@tcja/taxcalc/reforms/ext.json"
    salt_profile = {
        "ID_AllTaxes_c": {"2026":  [single_amount, single_amount*2, single_amount, single_amount, single_amount*2]},
    }
    model = TaxBrain(2026, 2035, microdata="TMD", base_policy=tcja_ext, reform=salt_profile, behavior={"sub": sub, "cg": cg})
    model.run()
    result_df = model.weighted_totals("combined") * 1e-12
    diff = result_df.iloc[2].sum(axis=0)
    output = {
        'single_amount': single_amount,
        'sub': sub,
        'cg': cg,
        'diff': diff
    }
    
    return output

# def calc_rev_diff(list1_single_amount):
#     output_list = []

#     for input_i in list1_single_amount:
#         single_amount_i = input_i
#         sub_i = 0
#         cg_i = 0
    
#         tcja_ext = "github://OFRA-ORG:Tax-Calculator-thru74@tcja/taxcalc/reforms/ext.json"
#         salt_profile = {
#             "ID_AllTaxes_c": {"2026":  [single_amount_i, single_amount_i*2, single_amount_i, single_amount_i, single_amount_i*2]},
#         }
#         model = TaxBrain(2026, 2035, microdata="TMD", base_policy=tcja_ext, reform=salt_profile, behavior={"sub": sub_i, "cg": cg_i})
#         model.run()
#         result_df = model.weighted_totals("combined") * 1e-12
#         diff = result_df.iloc[2].sum(axis=0)
    
#         output_i = {
#             'single_amount': single_amount_i,
#             'sub': sub_i,
#             'cg': cg_i,
#             'diff': diff
#         }
#         output_list.append(output_i)
            
#     return output_list

# def calc_rev_diff(input_list):
#     output_list = []

#     for input_i in input_list:
#         single_amount_i = input_i[0]
#         sub_i = input_i[1]
#         cg_i = input_i[2]
    
#         tcja_ext = "github://OFRA-ORG:Tax-Calculator-thru74@tcja/taxcalc/reforms/ext.json"
#         salt_profile = {
#             "ID_AllTaxes_c": {"2026":  [single_amount_i, single_amount_i*2, single_amount_i, single_amount_i, single_amount_i*2]},
#         }
#         model = TaxBrain(2026, 2035, microdata="TMD", base_policy=tcja_ext, reform=salt_profile, behavior={"sub": sub_i, "cg": cg_i})
#         model.run()
#         result_df = model.weighted_totals("combined") * 1e-12
#         diff = result_df.iloc[2].sum(axis=0)
    
#         output_i = {
#             'single_amount': single_amount_i,
#             'sub': sub_i,
#             'cg': cg_i,
#             'diff': diff
#         }
#         output_list.append(output_i)
            
#     return output_list
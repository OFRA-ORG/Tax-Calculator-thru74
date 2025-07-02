import time
from tqdm import tqdm
import pandas as pd
import numpy as np
from taxcalc.salt_functions import calc_rev_diff

sub = 0.25
cg = -3.45

start_time = time.time()

outputs = []
for single_amount in tqdm(np.linspace(0,10000,101)):
    diff_max = calc_rev_diff(single_amount, sub, cg, rate_adjust=0)
    
    def find_intercept(rate_adjust_i):
        diff_i = calc_rev_diff(single_amount, sub, cg, rate_adjust=rate_adjust_i)
        slope_i = (diff_i - diff_max)/rate_adjust_i
        rate_adjust_next = -diff_max/slope_i
    
        return diff_i, rate_adjust_next

    diff_i = 999
    rate_adjust_i = -0.012
    while abs(diff_i) > 0.0005:
        diff_i, rate_adjust_i = find_intercept(rate_adjust_i)
    rate_adjust_final = round(rate_adjust_i*1000000)/1000000
    rate_adjust_final_r1 = round(rate_adjust_i*100000)/100000
    rate_adjust_final_r2 = round(rate_adjust_i*10000)/10000

    print(str(single_amount)+'  ->  '+str(rate_adjust_final))
    
    output = {
        'single_amount': single_amount,
        'sub': sub,
        'cg': cg,
        'rate_adjust': rate_adjust_final,
        'rate_adjust_r1': rate_adjust_final_r1,
        'rate_adjust_r2': rate_adjust_final_r2
    }
    outputs.append(output)
    
df_outputs = pd.DataFrame(outputs)
df_outputs.to_pickle('./salt_iit_results/all.pkl')

print("Hours: " + str((time.time() - start_time)/3600))

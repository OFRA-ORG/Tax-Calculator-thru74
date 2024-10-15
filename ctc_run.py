import time
from tqdm import tqdm
import pandas as pd
import numpy as np
from salt_func import calc_rev_diff

sub = 0.25
cg = -3.45

start_time = time.time()

for single_amount in tqdm(np.linspace(0,10000,101)[40:]):

    if single_amount < 10000:    
        diff_max = calc_rev_diff(single_amount, sub, cg, ctc_adjust=0, with_penalty=True)
        
        def find_intercept(ctc_adjust_i):
            diff_i = calc_rev_diff(single_amount, sub, cg, ctc_adjust=ctc_adjust_i, with_penalty=True)
            slope_i = (diff_i - diff_max)/ctc_adjust_i
            ctc_adjust_next = -diff_max/slope_i
        
            return diff_i, ctc_adjust_next
    
        diff_i = 999
        ctc_adjust_i = 700
        while abs(diff_i) > 0.0005:
            diff_i, ctc_adjust_i = find_intercept(ctc_adjust_i)
        ctc_adjust_final = round(ctc_adjust_i)
        ctc_adjust_final_r5 = 5*round(ctc_adjust_i/5)
        ctc_adjust_final_r10 = 10*round(ctc_adjust_i/10)
    
        print(str(single_amount)+'  ->  '+str(ctc_adjust_final))
        
        output = {
            'single_amount': single_amount,
            'sub': sub,
            'cg': cg,
            'ctc_adjust': ctc_adjust_final,
            'ctc_adjust_r5': ctc_adjust_final_r5,
            'ctc_adjust_r10': ctc_adjust_final_r10
        }
        df = pd.DataFrame(output, index=[0])
        df.to_pickle('ctc_results/'+str(single_amount)+'.pkl')

    else:
        output = {
            'single_amount': single_amount,
            'sub': sub,
            'cg': cg,
            'ctc_adjust': 0,
            'ctc_adjust_r5': 0,
            'ctc_adjust_r10': 0
        }
        df = pd.DataFrame(output, index=[0])
        df.to_pickle('ctc_results/'+str(single_amount)+'.pkl')

print("Hours: " + str((time.time() - start_time)/3600))

import time
from tqdm import tqdm
import pandas as pd
import numpy as np
from salt_func import calc_rev_diff

sub = 0.25
cg = -3.45

start_time = time.time()

outputs = []
for single_amount, rate_adjust in tqdm(zip(np.linspace(0,10000,101)[17:17*2], np.linspace(-0.01,0,101)[17:17*2])):
    
    diff = 999
    while diff>0:
        diff = calc_rev_diff(single_amount, sub, cg, rate_adjust=rate_adjust, with_penalty=True)
        rate_adjust -= 0.001
    rate_adjust_1 = rate_adjust + 0.001*2 - 0.0001
    diff_1 = 999
    while diff_1>0:
        diff_1 = calc_rev_diff(single_amount, sub, cg, rate_adjust=rate_adjust_1, with_penalty=True)
        rate_adjust_1 -= 0.0001
    diff_fp = diff_1
    rate_adjust_fp = rate_adjust_1 + 0.0001
    
    output = {
        'single_amount': single_amount,
        'sub': sub,
        'cg': cg,
        'rate_adjust': rate_adjust_fp,
        'diff': diff_fp
    }
    outputs.append(output)
    
df_outputs = pd.DataFrame(outputs)
df_outputs.to_pickle('iit2.pkl')

print("Hours: " + str((time.time() - start_time)/3600))
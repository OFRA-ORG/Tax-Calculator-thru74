import time
from tqdm import tqdm
import pandas as pd
import numpy as np
from salt_func import calc_rev_diff

sub = 0.25
cg = -3.45

start_time = time.time()

outputs = []
for single_amount, sd_adjust in tqdm(zip(np.linspace(0,10000,101)[0:17], np.linspace(900,0,101)[0:17])):
    sd_adjust = np.ceil(sd_adjust/10)*10

    diff = -999
    while diff<0:
        diff = calc_rev_diff(single_amount, sub, cg, sd_adjust=sd_adjust, with_penalty=True)
        sd_adjust -= 50
    sd_adjust_1 = sd_adjust + 50*2 - 10
    diff_1 = -999
    while diff_1<0:
        diff_1 = calc_rev_diff(single_amount, sub, cg, sd_adjust=sd_adjust_1, with_penalty=True)
        sd_adjust_1 -= 10
    diff_fp = diff_1
    sd_adjust_fp = sd_adjust_1 + 10
    
    output = {
        'single_amount': single_amount,
        'sub': sub,
        'cg': cg,
        'sd_adjust': sd_adjust_fp,
        'diff': diff_fp
    }
    outputs.append(output)
    
df_outputs = pd.DataFrame(outputs)
df_outputs.to_pickle('sd1.pkl')

print("Hours: " + str((time.time() - start_time)/3600))
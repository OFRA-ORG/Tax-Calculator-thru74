#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from tqdm import tqdm
import pandas as pd
from salt_functions import calc_rev_diff, sim_salt


# In[2]:


sub = 0.25
cg = -3.45


# In[3]:


start_time = time.time()

for single_amount in tqdm(range(0, 10001, 100)):
    model = sim_salt(single_amount, sub, cg)
    
    result_df = model.weighted_totals("combined") * 1e-12
    diff = result_df.iloc[2].sum(axis=0)
    output = {
        'single_amount': single_amount,
        'sub': sub,
        'cg': cg,
        'diff': diff
    }
    df = pd.DataFrame(output, index=[0])
    df.to_pickle('salt_results/'+str(single_amount)+'.pkl')

    stats = []
    base_data = model.base_data
    reform_data = model.reform_data    
    for year in range(2025, 2036):
        stat = {
            'single_amount': single_amount,
            'sub': sub,
            'cg': cg,
            'year': year,
            'base_itemizers': sum(base_data[year]["s006"].where(base_data[year]["c04470"] > 0.0, 0.0)),
            'base_households': sum(base_data[year]["s006"]),
            'reform_itemizers': sum(reform_data[year]["s006"].where(reform_data[year]["c04470"] > 0.0, 0.0)),
            'reform_households': sum(reform_data[year]["s006"])
        }
        stats.append(stat)
    df_item = pd.DataFrame(stats)
    df_item.to_pickle('salt_results/'+str(single_amount)+'_itemizers.pkl')

print("Hours: " + str((time.time() - start_time)/3600))


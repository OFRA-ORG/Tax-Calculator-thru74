#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from tqdm import tqdm
import pandas as pd
from salt_func import calc_rev_diff


# In[2]:


sub = 0
cg = -2.45


# In[3]:


start_time = time.time()

outputs = []
for single_amount in tqdm(range(0, 10001, 50)):
    diff = calc_rev_diff(single_amount, sub, cg)
    output = {
        'single_amount': single_amount,
        'sub': sub,
        'cg': cg,
        'diff': diff
    }
    outputs.append(output)
df_outputs = pd.DataFrame(outputs)
df_outputs.to_pickle('salt1.pkl')

print("Hours: " + str((time.time() - start_time)/3600))


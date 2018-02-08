#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python2 version

import sys
import time
import pandas as pd

sip_str = "1-2-3-4-5"
g_output_df = pd.DataFrame(columns = ["hit_cnt", "dip", "dport", "proto","sip"])
new = pd.DataFrame([[1, 2, 3, 4,sip_str ]], columns=["hit_cnt", "dip", "dport", "proto", "sip"])
g_output_df = g_output_df.append(new,ignore_index=True)
print g_output_df
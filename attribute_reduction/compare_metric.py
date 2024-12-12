import os
import numpy as np
import pandas as pd
from Pfunc import *


concept_list = [8, 34, 68, 84]
metric_types = ['E', 'H', 'K', 'PC', 'Phi']
data_dir = '/home/huangdn/Attribute_Reduction/result'

D = ['subconcept']
result_list = []
for cpt in concept_list:
    print(f'In concept {cpt}...')
    table_name = f'concept_{cpt}_binary.xlsx'
    table_path = os.path.join('./data', table_name)
    table = pd.read_excel(table_path, index_col=0)
    C = list(table.columns[2:])
    funcs = Functional(filter_data(table))
    for mtc in metric_types:
        file_name = f'daar_funcs_concept_{cpt}_{mtc}.xlsx'
        file_path = os.path.join(data_dir, file_name)
        df = pd.read_excel(file_path)
        for att in df['Attribute_Set']:
            P = att.split(', ')
            E = funcs.E(D, P)
            E_C = funcs.E(D, C)
            H = funcs.H(D, P)
            H_C = funcs.H(D, C)
            K = funcs.K(D, P)
            K_C = funcs.K(D, C)
            PC = funcs.PC(D, P)
            PC_C = funcs.PC(D, C)
            Phi = funcs.Phi(D, P)
            Phi_C = funcs.Phi(D, C)
            result_list.append([cpt, mtc, att, E_C, H_C, K_C, PC_C, Phi_C, E, H, K, PC, Phi])
df = pd.DataFrame(
    result_list, 
    columns=[
        'concept', 'metric', 'attribute_set', 
        'E_C', 'H_C', 'K_C', 'PC_C', 'Phi_C', 
        'E', 'H', 'K', 'PC', 'Phi'
    ]
)
df.to_excel('./result/compare_metric.xlsx')

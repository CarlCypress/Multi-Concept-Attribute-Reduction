import os
import time
import json
from Pfunc import *
import pandas as pd


def DAAR(concept_idx, return_run_time=False):
    table_name = f'concept_{concept_idx}_binary.xlsx'
    table_path = os.path.join('/home/huangdn/Attribute_Reduction/data', table_name)
    table = pd.read_excel(table_path, index_col=0)

    start_time = time.time()

    funcs = Functional(filter_data(table))
    C = list(table.columns[2:])
    map_index = {value: index for index, value in enumerate(C)}
    D = ['subconcept']

    k = 1
    delta = [dict(), dict()]
    # only tuple type can store in set, so ...
    # explain delta structure: [{None}, {}, ..., {(), (), ...,(a1, a2,..., ak), ..., ()}, ..., {}].
    for ai in C:
        delta[k][tuple([ai])] = funcs.PC(D, [ai])  # Adding {ai} to delta_{size_k}
    while len(delta[k]):
        # print(f'In level {k}...', end=' ')
        # print(f'delta[{k}] = {delta[k]}.')
        delta.append(dict())  # init next delta_{k + 1}
        for Pi_tuple in delta[k].keys():
            Pi_list = list(Pi_tuple)
            max_index = map_index[Pi_list[-1]]
            for j in range(max_index + 1, len(C)):
                P_list = Pi_list.copy()
                P_list.append(C[j])
                P_tuple = tuple(P_list)
                # if len(funcs.POS(P_list, D)) > len(funcs.POS(Pi_list, D)) or funcs.PC(D, P_list) > delta[k][Pi_tuple]:
                    # print(f'Choose the {Pi_tuple} -> {P_tuple}. POS_Pi(D) = {funcs.POS(Pi_list, D)}, POS_P(D) = {funcs.POS(P_list, D)}; PC(D|Pi) = {funcs.PC(D, Pi_list)}, PC(D|P) = {funcs.PC(D, P_list)}.')
                delta[k + 1][P_tuple] = funcs.PC(D, P_list)
        k += 1

    _delta = dict()
    _delta[tuple(C)] = funcs.PC(D, C)

    for dct in delta:
        for key in dct.keys():
            _delta[key] = dct[key]
    max_value = max(_delta.values())
    delta = {k: v for k, v in _delta.items() if v == max_value}
    filtered_delta = filter_superset_keys(delta)
    end_time = time.time()
    if return_run_time:
        return end_time - start_time
    return filtered_delta


def execute(save_path):
    for idx in [8, 34, 68, 84]:
        delta = DAAR(idx)
        delta = {str(k): v for k, v in delta.items()}
        file_path = os.path.join(save_path, f'DAAR_of_concept{idx}.json')
        with open(file_path, 'w') as json_file:
            json.dump(delta, json_file, indent=4)  # indent参数可以美化输出
        print(f'DAAR_of_concept{idx}.json is Done.')
    pass


# path_to_result = '/home/huangdn/Attribute_Reduction/result'
# execute(path_to_result)

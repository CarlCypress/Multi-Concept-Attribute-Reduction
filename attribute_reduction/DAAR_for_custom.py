import os
import json
from Pfunc import *
import pandas as pd
from concurrent.futures import ProcessPoolExecutor


def DAAR_for_func(concept_idx, func_type: str):
    table_name = f'concept_{concept_idx}_binary.xlsx'
    table_path = os.path.join('/home/huangdn/Attribute_Reduction/data', table_name)
    table = pd.read_excel(table_path, index_col=0)
    funcs = Functional(filter_data(table))
    func_map = {
        "PC": funcs.PC,
        "Phi": funcs.Phi,
        "H": funcs.H,
        "E": funcs.E,
        "K": funcs.K
    }
    func = func_map[func_type]
    C = list(table.columns[2:])
    map_index = {value: index for index, value in enumerate(C)}
    D = ['subconcept']
    func_C = func(D, C)

    k = 1
    delta = [dict(), dict()]
    _delta = dict()
    # only tuple type can store in set, so ...
    # explain delta structure: [{None}, {}, ..., {(), (), ...,(a1, a2,..., ak), ..., ()}, ..., {}].
    # print('--------------------------------Start searching--------------------------------')
    for ai in C:
        delta[k][tuple([ai])] = func(D, [ai])  # Adding {ai} to delta_{size_k}
    while len(delta[k]):
        # print(f'In {k}th level, max have {_delta}.')
        delta.append(dict())  # init next delta_{k + 1}
        for Pi_tuple in delta[k].keys():
            Pi_list = list(Pi_tuple)
            max_index = map_index[Pi_list[-1]]
            for j in range(max_index+1, len(C)):
                P_list = Pi_list.copy()
                P_list.append(C[j])
                P_tuple = tuple(P_list)
                func_P = func(D, P_list)
                if func_P == func_C:
                    _delta[P_tuple] = func_P
                # else:
                delta[k + 1][P_tuple] = func_P
                pass
            pass
        k += 1
    res_delta = dict()
    # print('--------------------------------End searching--------------------------------')
    # print(f'Equal max have {_delta}.')
    # print('--------------------------------Check search--------------------------------')
    for Pi_tuple in _delta.keys():
        # print(f'For Att set {Pi_tuple}, the sub att set situation is: ')
        lower_subsets = [Pi_tuple[:i] + Pi_tuple[i+1:] for i in range(len(Pi_tuple))]
        func_lower_subsets = {subset: func(D, list(subset)) for subset in lower_subsets}
        # print(func_lower_subsets)
        all_greater = all(value > func_C for value in func_lower_subsets.values())
        if all_greater:
            res_delta[Pi_tuple] = func_C
    # print('--------------------------------Finish check search--------------------------------')
    # print(f'However, the result max have {res_delta}.')
    return res_delta


def process_task(concept_idx, func_type, save_path):
    delta = DAAR_for_func(concept_idx, func_type)
    df = pd.DataFrame({
        "Attribute_Set": [", ".join(key) for key in delta.keys()],
        func_type: list(delta.values())
    })
    output_file = os.path.join(save_path, f'daar_funcs_concept_{concept_idx}_{func_type}.xlsx')
    df.to_excel(output_file, index=False)
    print(f"Saved: {output_file}")


def execute_daar_for_others_func(save_path='/home/huangdn/Attribute_Reduction/result', max_workers=16):
    concept_list = [8, 34, 68, 84]
    funcs_list = ["Phi", "H", "E", "K"]

    # 准备所有任务
    tasks = [(cpt, fc_tp, save_path) for cpt in concept_list for fc_tp in funcs_list]

    # 使用 ProcessPoolExecutor 进行多进程处理
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_task, cpt, fc_tp, save_path) for cpt, fc_tp, save_path in tasks]

        # 等待所有任务完成
        for future in futures:
            future.result()  # 如果需要捕获异常，可以在这里处理

    print("All tasks completed.")


execute_daar_for_others_func()
# DAAR_for_func(68, 'K')

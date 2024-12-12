import os
import time
import random
from Pfunc import *
import pandas as pd


def heuri(concept_idx, search_times=500, optimization_unit=100, return_run_time=False):
    table_name = f'concept_{concept_idx}_binary.xlsx'
    table_path = os.path.join('./data', table_name)
    table = pd.read_excel(table_path, index_col=0)

    start_time = time.time()

    funcs = Functional(filter_data(table))
    C = set(table.columns[2:])
    D = ['subconcept']
    delta = {
        k: funcs.PC(D, list(k))
        for k in set([
            tuple(sorted(random.sample(list(C), golden_ratio(len(C)))))
            for rp in range(10)
        ])
    }  # init 10 attribute set.
    _ = delta.copy()  # for check init state.
    for t in range(1, search_times+1):
        if t % optimization_unit == 0:
            max_pc = max(delta.values())
            att_tus = [key for key, value in delta.items() if value == max_pc]
        else:
            att_tus = [random.choice(list(delta.keys()))]
        for att_tu in att_tus:
            att_set = set(att_tu)
            s = C - att_set
            # expand element.
            for col in s:
                expand = tuple(sorted(att_set | {col}))
                if expand in delta.keys():
                    continue
                delta[expand] = funcs.PC(D, list(expand))
            # shrink element
            for col in att_set:
                shrink = tuple(sorted(att_set - {col}))
                if len(shrink) == 0 or shrink in delta.keys():
                    continue
                delta[shrink] = funcs.PC(D, list(shrink))
    # filter PC value == max{PC}.
    max_pc = max(delta.values())
    delta = {k: v for k, v in delta.items() if v == max_pc}
    filtered_delta = filter_superset_keys(delta)
    end_time = time.time()
    if return_run_time:
        return end_time - start_time
    return _, filtered_delta


# def heuri(concept_idx, search_times=500):
#     table_name = f'concept_{concept_idx}_binary.xlsx'
#     table_path = os.path.join('./data', table_name)
#     table = pd.read_excel(table_path, index_col=0)
#     funcs = Functional(filter_data(table))
#     C = set(table.columns[2:])
#     D = ['subconcept']
#     delta = {
#         k: funcs.PC(D, list(k)) 
#         for k in set([
#             tuple(sorted(random.sample(list(C), golden_ratio(len(C))))) 
#             for rp in range(10)
#         ])
#     }  # init 10 attribute set.
#     _ = delta.copy()  # for check init state.
#     for t in range(search_times):
#         att_tu = random.choice(list(delta.keys()))
#         att_set = set(att_tu)
#         s = C - att_set
#         # expand element.
#         for col in s:
#             expand = tuple(sorted(att_set | {col}))
#             if expand in delta.keys():
#                 continue
#             delta[expand] = funcs.PC(D, list(expand))
#         # shrink element
#         for col in att_set:
#             shrink = tuple(sorted(att_set - {col}))
#             if len(shrink) == 0 or shrink in delta.keys():
#                 continue
#             delta[shrink] = funcs.PC(D, list(shrink))
#     # filter PC value == max{PC}.
#     max_pc = max(delta.values())
#     delta = {k: v for k, v in delta.items() if v == max_pc}
#     return _, filter_superset_keys(delta)

    # delta = {}
    # for col in C:
    #     delta[tuple([col])] = funcs.PC(D, [col])
    # for t in range(search_times):
    #     length = len(delta)
    #     key_list = get_top_n_keys(delta, length, False)
    #     div = init_div_list(length, n)
    #     choice_list = init_choice_list(div, key_list, n)
    #     random_tuple = random.choice(choice_list)
    #     s = C - set(random_tuple)
    #     for col in s:
    #         li = list(random_tuple)
    #         li.append(col)
    #         li = sorted(li)
    #         tl = tuple(li)
    #         if tl in delta.keys():
    #             continue
    #         delta[tl] = funcs.PC(D, li)
    #     pass

    # max_value = max(delta.values())
    # # 筛选出所有与最大值相等的 key, value 对，并保存为字典
    # delta = {k: v for k, v in delta.items() if v == max_value}
    # return filter_superset_keys(delta)


# print(heuri(84, 10)[-1])


# def execute(save_path='/home/huangdn/Attribute_Reduction/result'):
#     _, delta = heuri(-1, search_times=3000, optimization_unit=10)
#     delta = {str(k): v for k, v in delta.items()}
#     file_path = os.path.join(save_path, 'merge_reduction.json')
#     with open(file_path, 'w') as json_file:
#         json.dump(delta, json_file, indent=4)  # indent参数可以美化输出
#     print('merge_reduction.json is Done.')
#     pass


# execute()


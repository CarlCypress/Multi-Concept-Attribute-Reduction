# -*- coding: utf-8 -*-
# @Time : 2024/9/30 上午12:16
# @Author : D.N. Huang
# @Email : CarlCypress@yeah.net
# @File : use_heuri.py
# @Project : Attribute_Reduction
import os
import ast
import json
import logging
import pandas as pd
from Pfunc import *
from Heuri import heuri
from concurrent.futures import ProcessPoolExecutor


repetitions = 10
concept_list = [8, 34, 68, 84]
search_time_list = [200, 400, 500, 600, 800, 1500, 2500, 3500, 4500]
optimization_node = [10, 20, 30, 40, 50]


def process(concept_idx, search_times=500, optimization_unit=100):
    json_path = f'./result/DAAR_of_concept{concept_idx}.json'
    with open(json_path, 'r') as f:
        data_dict = json.load(f)
    data_dict = {ast.literal_eval(k): v for k, v in data_dict.items()}
    ground_truth = set(data_dict.keys())
    init, delta = heuri(concept_idx, search_times, optimization_unit)
    save_heuri_result(concept_idx, search_times, delta, init, file_path=f'./logs/predict{concept_idx}.txt')
    predict = set(delta.keys())
    intersect = predict & ground_truth
    precision = len(intersect) / len(predict)
    recall = len(intersect) / len(ground_truth)
    f1 = 0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def main(concept_idx, save_path='./'):
    logging.basicConfig(filename=os.path.join(save_path, f'output{concept_idx}.log'), level=logging.INFO, 
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        force=True)
    result = []
    for opt_node in optimization_node:
        for search_times in search_time_list:
            bar_precisoin, bar_recall, bar_f1 = 0, 0, 0
            for rep in range(repetitions):
                evaluation = process(concept_idx, search_times, opt_node)
                precision = evaluation['precision']
                recall = evaluation['recall']
                f1 = evaluation['f1']
                bar_precisoin += precision
                bar_recall += recall
                bar_f1 += f1
                info = f'Rep {rep+1}, Concept={concept_idx}, optimization_unit={opt_node}, search_times={search_times}, precision={precision}, recall={recall}, f1={f1}.'
                logging.info(info)
            bar_precisoin /= repetitions
            bar_recall /= repetitions
            bar_f1 /= repetitions
            cell = {
                'Concept': concept_idx,
                'Optimization_Unit': opt_node, 
                'Search_Times': search_times, 
                'Precision': bar_precisoin, 
                'Recall': bar_recall, 
                'F1': bar_f1 
            }
            result.append(cell)
            logging.info('Avg, ' + str(cell))
    df = pd.DataFrame(result)
    df.to_excel(os.path.join(save_path, f'evaluation{concept_idx}.xlsx'), index=False)


with ProcessPoolExecutor(max_workers=4) as executor:
    executor.map(main, concept_list, ['logs'] * len(concept_list))

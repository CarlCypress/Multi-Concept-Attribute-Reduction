import pandas as pd
from DAAR import DAAR
from Heuri import heuri


concepts_list = [8, 34, 68, 84]
search_times = [1000, 2000, 3000, 4000, 5000]
optimization_units = [10, 20, 30, 40, 50]
results_record = []
for cpt in concepts_list:
    print(f'In concept {cpt}:')
    # daar_time = DAAR(cpt, return_run_time=True)
    # row_data = {"concept": cpt, "DAAR_runtime": daar_time}
    row_data = {"concept": cpt}
    for stime in search_times:
        for oms in optimization_units:
            heuri_time = heuri(concept_idx=cpt, search_times=stime, optimization_unit=oms, return_run_time=True)
            row_data[f"Heuri_t{stime}_o{oms}_runtime"] = heuri_time
            print(f'search time is {stime}, optimization unit is {oms}, runtime is {heuri_time}.')
    results_record.append(row_data)
df = pd.DataFrame(results_record)
df.to_excel("./result/runtime_t2.xlsx", index=False)


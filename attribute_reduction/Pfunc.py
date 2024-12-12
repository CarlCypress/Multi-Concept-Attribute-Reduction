import math
import pandas as pd


def golden_ratio(n: int):
    """calucation gloden ratio of n, and return small one floor of b.
    """
    phi = 1.618
    b = n / (1 + phi)
    return math.floor(b)


def filter_data(df) -> pd.DataFrame:
    """
    过滤无实例的概念(行)。
    """
    return df.loc[df['subconcept'] != '-1', :]


def equal_class(df: pd.DataFrame, col_list: list) -> list:
    """
    计算 `[x]_p` ，即等价类。
    :param df: 被计算的table。
    :param col_list: 集族p(因python无法用set类型表示集族，故用list)。
    :return: 返回 `[df]_{col_list}` 的计算结果。
    """
    grouped = df.groupby(col_list)['instance'].apply(set).tolist()
    return grouped


def filter_superset_keys(delta):
    """
    过滤掉字典中那些是其他键的超集的键，返回新的字典。

    参数:
        delta (dict): 需要过滤的字典，其键为元组。
    返回:
        dict: 只包含没有更小子集的键的过滤后的字典。
    """
    # 获取所有键
    keys = list(delta.keys())
    # 保留结果的集合
    result_keys = set(keys)
    # 对每一对键进行比较，找出超集并删除
    for i in range(len(keys)):
        for j in range(len(keys)):
            if i != j:
                # 如果 keys[i] 是 keys[j] 的超集，删除 keys[i]
                if set(keys[i]).issuperset(set(keys[j])):
                    result_keys.discard(keys[i])
    # 构建新的 delta 字典，只保留符合条件的键
    filtered_delta = {k: delta[k] for k in result_keys}
    
    return filtered_delta


# def POS(P, Q) -> set:
#     res = set()
#     for e1 in P:
#         for e2 in Q:
#             if e1.issubset(e2):
#                 for e in e1:
#                     res.add(e)
#                 break
#     return res


# def PS(P, Q) -> float:
#     m, n = len(P), len(Q)
#     Avg = (m + n) / 2
#     Sum = 0
#     for e1 in P:
#         for e2 in Q:
#             Sum += len(e1 & e2) / len(e1 | e2)
#     return Sum / Avg


# def PC(P, Q, U) -> float:
#     return len(POS(Q, P)) * PS(P, Q) / U  # 此处调用不对，应该是POS(Q, P)


def get_top_n_keys(dct, n, is_sort=True) -> list:
    """以list的形式返回dct中value前n个大的keys。"""
    # 根据字典的value对字典进行排序
    sorted_keys = sorted(dct, key=dct.get, reverse=True)
    # 取出前n个排序后的键
    top_n_keys = sorted_keys[:n]
    # 返回按照字母序排序的集合
    if is_sort:
        return sorted(top_n_keys)  # 这会影响list与value原本大小的顺序关系
    return top_n_keys


def get_nth_largest_key(d: dict, n: int) -> tuple:
    """返回字典d中value第n大的keys。"""
    # 根据字典的值对键进行排序
    sorted_keys = sorted(d, key=d.get, reverse=True)
    # 获取第n大的键
    nth_largest_key = sorted_keys[n - 1] if len(sorted_keys) >= n else None
    return nth_largest_key


def init_set(dct: dict, n: int) -> set:
    """返回dct中value分别为第1,2,...,n大的keys。"""
    res = set()
    for i in range(1, n + 1):
        res.add(get_nth_largest_key(dct, i))
        pass
    return res


def init_div_list(length: int, n: int) -> list:
    """
    将 `length` '均分'成 `n` 个元素。
    即返回长度为 `n` 的list，第i个元素代表第i批的元素个数。
    """
    down = length // n
    div = [down for i in range(n)]
    leave, idx = length - down * n, n - 1
    # 下面对严格均分后的list末尾添加剩余元素，直至length个元素添加完成
    while leave > 0:
        div[idx] += 1
        leave -= 1
        idx -= 1
        pass
    return div


def init_choice_list(div, key_list, n) -> list:
    """
    按照 div 当中 `n` 批元素的个数，将key_list当中的元素进行分开。
    第 `i` 批元素当中的元素需要重复 `n-i` 次。
    """
    choice_list = list()
    idx = 0
    for i in range(n):
        while div[i] > 0:
            cnt = n - i  # 前面批次当中的元素数量会重复多次，如第1批中每个元素重复5次，第2批中每个元素重复4次...
            while cnt > 0:
                choice_list.append(key_list[idx])
                cnt -= 1
            div[i] -= 1
            idx += 1
    return choice_list


def C(n: int, k: int) -> int:
    """计算 `C^k_n` ，即组合数。"""
    if n == 0 or n < k:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def C2(n: int) -> int:
    """默认k=2的实现方法"""
    return n * (n - 1) // 2


class Functional:
    """此类实现 `[x]_P, POS_P(D), PS([x]_p, [x]_D), PC(D|P)` 等函数。"""

    def __init__(self, table: pd.DataFrame):
        self.df = table
        self.u = self.df['instance'].values.tolist()

    def equal_class(self, col_list: list) -> list:
        """
        计算 `[x]_P` ，即等价类。
        :param col_list: 集族p(因python无法用set类型表示集族，故用list)。
        :return: 返回 `[df]_{col_list}` 的计算结果。
        """
        grouped = self.df.groupby(col_list)['instance'].apply(set).tolist()
        return grouped

    def equal_class_for_D(self, col_list: list) -> list:
        """此处专为`subconcept`列专门计算`[x]_D`，其中分类方式存在差别。(函数名中d指subconcept)"""
        df_expanded = self.df.assign(d_split=self.df[col_list[0]].str.split(',')).explode('d_split')
        grouped = df_expanded.groupby('d_split')['instance'].apply(set).tolist()
        return grouped

    def POS(self, P: list, D: list) -> set:
        """
        计算 `POS_P(D)` ，其中 `P, D` 为属性集合。
        `POS_P(D)` 计算的是 `[x]_P` 当中的集合包含于 `[x]_D` 当中的集合当中的元素。
        :param P: 属性集P。
        :param D: 属性集D。
        :return: POS_P(D)
        """
        Xp = self.equal_class(P)
        # Xd = self.equal_class(D)
        Xd = self.equal_class_for_D(D)
        POSpd = set()
        for e1 in Xp:
            for e2 in Xd:
                if e1.issubset(e2):
                    for e in e1:
                        POSpd.add(e)
                    break
        return POSpd

    def PS(self, Xp: list, Xd: list) -> float:
        """
        计算 `PS([x]_P, [x]_D)` ，其中 `[x]_P, [x]_D` 为等价类。
        PS([x]_P, [x]_D) = \frac{1}{avg(m, n)}\sum^m_{i=1}\sum^n_{j=1}\frac{|X_i\cap Y_j|}{|X_i\cup Y_j|}
        :param Xp: 属性集 `P` 的等价类。
        :param Xd: 属性集 `D` 的等价类。
        :return: PS([x]_P, [x]_D)。
        """
        # m, n = len(Xp), len(Xd)
        # Avg = (m + n) / 2
        Sum = 0
        for e1 in Xp:
            for e2 in Xd:
                Sum += (len(e1 & e2) ** 2) / len(e1 | e2)
                # Sum += len(e1 & e1) / len(e1 | e2)
        # return Sum / Avg
        return Sum / len(self.u)

    def PC(self, D: list, P: list) -> float:
        """
        计算 `PC(D|P)` ，其中 `D, P` 为属性集。
        :param D: 属性集D。
        :param P: 属性集P。
        :return: PC(D|P)。
        """
        # return len(self.POS(P, D)) * self.PS(self.equal_class(P), self.equal_class(D)) / len(self.u)
        return len(self.POS(P, D)) * self.PS(self.equal_class(P), self.equal_class_for_D(D)) / len(self.u)

    def Phi(self, D: list, P: list) -> float:
        """
        计算 `\Phi(D|P)` ，即不一致率，其中 `D, P` 为属性集。
        :param D: 属性集D。
        :param P: 属性集P。
        :return: \Phi(D|P)。
        """
        # Xp, Xd = self.equal_class(P), self.equal_class(D)
        Xp, Xd = self.equal_class(P), self.equal_class_for_D(D)
        Sum = 0
        for Xi in Xp:
            Max = -1
            for Yj in Xd:
                Max = max(Max, len(Xi & Yj))
            Sum += len(Xi) - Max
        return Sum / len(self.u)

    def H(self, D: list, P: list) -> float:
        """
        计算 `H(D|P)` ，即香农熵，其中 `D, P` 为属性集。
        :param D: 属性集D。
        :param P: 属性集P。
        :return: H(D|P)。
        """
        # Xp, Xd = self.equal_class(P), self.equal_class(D)
        Xp, Xd = self.equal_class(P), self.equal_class_for_D(D)
        Sum = 0
        for Xi in Xp:
            for Yj in Xd:
                if len(Xi & Yj) != 0:
                    Sum += len(Xi & Yj) * math.log2(len(Xi & Yj) / len(Xi))
        return -Sum / len(self.u)

    def E(self, D: list, P: list) -> float:
        """
        计算 `E(D|P)` ，即互补条件熵，其中 `D, P` 为属性集。
        :param D: 属性集D。
        :param P: 属性集P。
        :return: E(D|P)。
        """
        # Xp, Xd = self.equal_class(P), self.equal_class(D)
        Xp, Xd = self.equal_class(P), self.equal_class_for_D(D)
        Sum = 0
        for Xi in Xp:
            for Yj in Xd:
                Sum += len(Xi & Yj) * len(Xi - Yj)
        return Sum / math.pow(len(self.u), 2)

    def K(self, D: list, P: list) -> float:
        """
        计算 `K(D|P)` ，即组合条件熵，其中 `D, P` 为属性集。
        :param D: 属性集D。
        :param P: 属性集P。
        :return: K(D|P)。
        """
        # Xp, Xd = self.equal_class(P), self.equal_class(D)
        Xp, Xd = self.equal_class(P), self.equal_class_for_D(D)
        # [print(len(Yj)) for Yj in Xd]
        # print(len(self.u))
        # print(f'[X]p is {Xp}, [X]d is {Xd}, U is {self.u}:')
        Sum = 0
        # idx = 1
        for Xi in Xp:
            # print(f'index={idx},', end=' ')
            add_sum = len(Xi) * C2(len(Xi)) / (len(self.u) * C2(len(self.u)))
            Sum += add_sum
            # Sum += len(Xi) * C2(len(Xi)) / (len(self.u) * C2(len(self.u)))
            # print(f'{add_sum}', end=' ')
            # sub_sum = 0
            for Yj in Xd:
                # sub_sum += (len(Xi & Yj) * C2(len(Xi & Yj))) / (len(self.u) * C2(len(self.u)))
                Sum -= (len(Xi & Yj) * C2(len(Xi & Yj))) / (len(self.u) * C2(len(self.u)))
            # Sum -= sub_sum
            # print(f'- {sub_sum} = {add_sum - sub_sum}.')
            # if idx == 60:
            #     print(f'|U| = {len(self.u)}, C^2_U = {(len(self.u) * C2(len(self.u)))}')
            #     print(f'|X60| = {len(Xi)}, C^2_|X60| = {C2(len(Xi))}, add is {len(Xi) * C2(len(Xi)) / (len(self.u) * C2(len(self.u)))}')
            #     [print(f'|X60 & Y{i+1}| = {len(Xi & Yj)}, C^2_|X60 & Y{i+1}| = {C2(len(Xi & Yj))}, sub is {(len(Xi & Yj) * C2(len(Xi & Yj))) / (len(self.u) * C2(len(self.u)))}') for i, Yj in enumerate(Xd)]
            # idx += 1
        return Sum


def save_heuri_result(concept_idx, search_times, heuri_result, heuri_init, file_path='./logs/predict.txt'):
    with open(file_path, 'a') as f:
        # 写入title信息
        f.write(f"Concept Index: {concept_idx}, Search Times: {search_times}\n")
        f.write('Init 10 attribute set:\n')
        for key, value in heuri_init.items():
            f.write(f"{key}: {value}\n")
        f.write('predicted attribute set:\n')
        # 写入heuri结果中的key-value对
        for key, value in heuri_result.items():
            f.write(f"{key}: {value}\n")
        # 分隔不同heuri结果
        f.write("\n" + "-"*40 + "\n\n")
    f.close()


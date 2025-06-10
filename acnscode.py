from math import factorial
import random
import numpy as np
import hashlib
import time
import logging
import os
import psutil
# from memory_profiler import profile

# 配置日志记录
# logging.basicConfig(
#     filename="/app/logs/acnsall.log",  # 指定容器内的挂载路径
#     level=logging.INFO,
#     format="%(message)s",
# )

# @profile
def ACNSALL(num):
    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))

    def find_parties(gid, t, T):
        """
        根据 gid、t 和 T 找到对应的元素集合。

        参数:
        gid (int): 组的 ID。
        t (int): 需要选择的元素个数。
        T (int): 总元素个数。

        返回:
        list: 包含选中的元素的列表。
        """
        pt = []  # 用于存储结果
        mem = 0  # 已选元素个数

        for i in range(1, T):
            # 计算组合数 C(T - i, t - mem - 1)
            tmp = comb(T - i, t - mem - 1)

            if gid > tmp:
                gid -= tmp  # 跳过当前元素
            else:
                pt.append(i)  # 将当前元素加入结果集
                mem += 1  # 更新已选元素个数

            # 如果剩余元素个数加上已选元素个数等于 t，则将剩余元素全部加入结果集
            if mem + (T - i) == t:
                for j in range(i + 1, T + 1):
                    pt.append(j)
                break

        return pt

    def find_group_id(parties, t, T):
        """
        根据选中的元素集合 parties，计算其组 ID。

        参数:
        parties (list): 选中的元素集合，例如 [1, 3, 5]。
        t (int): 需要选择的元素个数。
        T (int): 总元素个数。

        返回:
        int: 组 ID。
        """
        mem = 0  # 已选元素个数
        group_count = 1  # 组 ID，初始值为 1

        for i in range(1, T + 1):
            if i in parties:
                mem += 1  # 当前元素在 parties 中，增加已选元素个数
            else:
                # 当前元素不在 parties 中，计算组合数并累加到 group_count
                group_count += comb(T - i, t - mem - 1)

            # 如果已选元素个数等于 t，则停止遍历
            if mem == t:
                break

        return group_count

    def share_secret_tTL(t, T, key, n, q):

        group_count = comb(T, t)  # 计算组合数 C(T, t)
        shared_key_repo_tT = {}  # 共享密钥仓库

        for gid in range(1, group_count + 1):
            # 找到当前组 ID 对应的参与方集合
            parties = find_parties(gid, t, T)

            # 初始化 shared_key_repo_tT 的嵌套字典
            for party in parties:
                if party not in shared_key_repo_tT:
                    shared_key_repo_tT[party] = {}
                if gid not in shared_key_repo_tT[party]:
                    shared_key_repo_tT[party][gid] = [0] * n

            # 将 key 复制到 shared_key_repo_tT[parties[0]][gid]
            shared_key_repo_tT[parties[0]][gid] = key.copy()

            # 对于其他参与方，生成随机向量并累加到 shared_key_repo_tT[parties[0]][gid]
            for i in range(1, t):
                shared_key_repo_tT[parties[i]][gid] = [
                    random.randint(0, 100) for _ in range(n)
                ]  # 随机生成向量
                for j in range(n):
                    shared_key_repo_tT[parties[0]][gid][j] += (
                        shared_key_repo_tT[parties[i]][gid][j] % q
                    )

        return shared_key_repo_tT

    def Hashf(stri, q, n):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(stri.encode("utf-8"))
        res = []
        for i in range(n):
            index = int(i)
            sha256_hash.update(
                index.to_bytes((index.bit_length() + 7) // 8, byteorder="big")
            )
            hash_hex = sha256_hash.hexdigest()
            val = int(hash_hex[:20], 16)
            res += [val % q]
        return res

    N = 3 * num + 1
    K = 2 * num + 1
    n = 412
    q = 2**31 - 1
    q1 = 268435456
    p = 2
    print("N:", N)
    logging.info(f"N: {N}")
    ###Sharing
    start_time = time.time()
    veck = np.random.randint(0, q, size=(1, n))[0]

    sharings = share_secret_tTL(K, N, veck, n, q)
    # print(sharings)
    end_time1 = time.time()
    # print(sharings)
    ###PartialEval
    vecx = "a random string as input a"
    hx = Hashf(vecx, q, n)
    pvalall = []
    for ent in range(1, N + 1):
        pvalent = []
        for k, v in sharings[ent].items():
            rowval = [k]
            hxkey = np.dot(hx, v) % q
            rowval += [np.round(hxkey * q1 / q).astype(int) % q1]
            pvalent += [rowval]
        pvalall += [pvalent]
    # print("pvalall",pvalall)
    end_time2 = time.time()
    print("PEval:", end_time2 - end_time1)
    logging.info(f"PEval: {end_time2-end_time1}")
    ###FinalEval
    V = [i for i in range(1, K + 1)]
    ind = find_group_id(V, K, N)
    # print("ind",ind)
    res = 0
    for rows in pvalall[V[0]]:  ##确保V[0]是V集合中最小的
        # print("rows",rows)
        if rows[0] == ind:
            res = rows[1:][0]
            break
    for i in range(1, K):
        for rows in pvalall[V[i]]:  ##确保V[0]是V集合中最小的
            if rows[0] == ind:
                res -= rows[1:][0] % q
                break
    final = np.round(res * p / q1).astype(int) % p
    end_time3 = time.time()
    print("FinalEval:", end_time3 - end_time2)
    logging.info(f"FinalEval: {end_time3-end_time2}")
    ###Eval
    cor = np.round(np.dot(hx, veck) * p / q).astype(int) % p
    # print("final",final)
    # print("cor",cor)
    # print(end_time3-end_time2,end_time2-end_time1,end_time1-start_time)

pid = os.getpid()
p = psutil.Process(pid)

for i in range(1, 14):
    ACNSALL(i)
    mem = p.memory_info().rss / (1024*1024)
    print(f"Current memory usage: {mem:.2f} MB")

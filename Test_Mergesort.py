import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr, l, r):
    if l < r:
        m = int((l + (r - 1)) / 2)
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


def Paramerge(L: list, R: list) -> list:
    n1 = len(L)
    n2 = len(R)
    if n1 == 0 and n2 == 0:
        return []
    res = [0 for x in range(len(L + R))]
    i = 0
    j = 0
    k = 0
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            res[k] = L[i]
            i += 1
        else:
            res[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        res[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        res[k] = R[j]
        j += 1
        k += 1
    return res


def ParallelMergesort(th_pool: ThreadPoolExecutor, data: list, l: int,
                      r: int) -> list:
    th_list = []
    data0 = data
    if (len(data0) == 1):
        return th_list, [data0[0]]
    if (len(data0) == 0):
        return th_list, th_list
    m = int((l + (r - 1)) / 2)
    data1 = data[0:m + 1]
    data2 = data[m + 1:r + 1]
    th1 = th_pool.submit(ParallelMergesort, th_pool, data1, 0, m)
    th2 = th_pool.submit(ParallelMergesort, th_pool, data2, 0, r - m - 1)
    res1 = [th1]
    res2 = [th2]
    wait(res1)
    for item in as_completed(res1):
        T1, R1 = item.result()
    wait(res2)
    for item in as_completed(res2):
        T2, R2 = item.result()
    R = Paramerge(R1, R2)
    return th_list, R


def main():
    pool = ThreadPoolExecutor(max_workers=30000)
    f = open('random.txt')
    lines = f.read()
    lines = lines.split(" ")
    nums = [int(x) for x in lines]
    f.close()
    begin_time_para = time.time()
    Thlist, res = ParallelMergesort(pool, nums, 0, len(nums) - 1)
    wait(Thlist)
    end_time_para = time.time()
    run_time_para = end_time_para - begin_time_para
    print("并行归并执行时间：", run_time_para)
    res_f1 = open('./result/order5.txt', 'w')
    for x in res:
        res_f1.write(str(x) + ' ')
    res_f1.close()
    begin_time = time.time()
    mergeSort(nums, 0, len(nums) - 1)
    end_time = time.time()
    run_time = end_time - begin_time
    print("串行归并执行时间：", run_time)
    res_f2 = open('./result/order6.txt', 'w')
    for x in nums:
        res_f2.write(str(x) + ' ')
    res_f2.close()


if __name__ == "__main__":
    main()
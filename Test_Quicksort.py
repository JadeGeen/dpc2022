import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

def partition(data: list, l: int, r: int) -> int:
    x = data[r]
    i = l - 1
    for j in range(l, r):
        if data[j] <= x:
            i = i + 1
            tmp = data[i]
            data[i] = data[j]
            data[j] = tmp
    tmp = data[i + 1]
    data[i + 1] = data[r]
    data[r] = tmp
    #print(data, end="\n")
    return i + 1


#串行
def QuickSort(data: list, l: int, r: int) -> None:
    if (l < r):
        p = partition(data, l, r)
        QuickSort(data, l, p - 1)
        QuickSort(data, p + 1, r)


#并行
def ParallelQuickSort(th_pool: ThreadPoolExecutor, data: list, l: int,
                      r: int) -> list:

    th_list = []
    data0 = data
    if (len(data0) == 1):
        return th_list, [data0[0]]
    if (len(data0) == 0):
        return th_list, th_list
    p = partition(data0, l, r)
    data1 = data0[0:p]
    data2 = data0[p + 1:r + 1]
    th1 = th_pool.submit(ParallelQuickSort, th_pool, data1, 0, p - 1)
    th2 = th_pool.submit(ParallelQuickSort, th_pool, data2, 0, r - p - 1)
    th_list.append(th1)
    th_list.append(th2)
    res1 = [th1]
    res2 = [th2]
    wait(res1)
    for item in as_completed(res1):
        T1, R1 = item.result()
        # print(R1, end="\n")
    wait(res2)
    for item in as_completed(res2):
        T2, R2 = item.result()
        # print(R2, end="\n")
    tmp = [
        data0[p],
    ]  #未被分入data1和2的privot
    R = R1 + tmp + R2
    return th_list, R


def main():
    pool = ThreadPoolExecutor(max_workers=30000)
    f = open('random.txt')
    lines = f.read()
    lines = lines.split(" ")
    nums = [int(x) for x in lines]
    f.close()
    begin_time_para = time.time()
    Thlist, res = ParallelQuickSort(pool, nums, 0, len(nums) - 1)
    wait(Thlist)
    end_time_para = time.time()
    run_time_para = end_time_para - begin_time_para
    print("并行快排执行时间：", run_time_para)
    res_f1 = open('./result/order1.txt', 'w')
    for x in res:
        res_f1.write(str(x) + ' ')
    res_f1.close()
    begin_time = time.time()
    QuickSort(nums, 0, len(nums) - 1)
    end_time = time.time()
    run_time = end_time - begin_time
    print("串行快排执行时间：", run_time)
    res_f2 = open('./result/order2.txt', 'w')
    for x in nums:
        res_f2.write(str(x) + ' ')
    res_f2.close()

if __name__ == "__main__":
    main()
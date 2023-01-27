import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed


#串行
def Enumeratesort(data: list) -> list:
    res = [0 for x in range(len(data))]
    for i in range(len(data)):
        count = 0
        for j in range(len(data)):
            if (j == i):
                continue
            if (data[j] < data[i]):
                count = count + 1
        res[count] = data[i]
    return res


def SingleEnumerate(data: list, index: int) -> int:
    count = 0
    for j in range(len(data)):
        if (j == index):
            continue
        if (data[j] < data[index]):
            count = count + 1
    return count, index


#并行
def ParallelEnumeratesort(th_pool: ThreadPoolExecutor, data: list) -> list:
    th_list = []
    for i in range(len(data)):
        th = th_pool.submit(SingleEnumerate, data, i)
        th_list.append(th)
    wait(th_list)
    res = [0 for x in range(len(data))]
    for item in as_completed(th_list):
        count, index = item.result()
        res[count] = data[index]
    return res


def main():
    pool = ThreadPoolExecutor(max_workers=30000)
    f = open('random.txt')
    lines = f.read()
    lines = lines.split(" ")
    nums = [int(x) for x in lines]
    f.close()
    begin_time_para = time.time()
    res_para = ParallelEnumeratesort(pool, nums)
    end_time_para = time.time()
    run_time_para = end_time_para - begin_time_para
    print("并行枚举执行时间：", run_time_para)
    res_f1 = open('./result/order3.txt', 'w')
    for x in res_para:
        res_f1.write(str(x) + ' ')
    res_f1.close()
    begin_time = time.time()
    res = Enumeratesort(nums)
    end_time = time.time()
    run_time = end_time - begin_time
    print("串行枚举执行时间：", run_time)
    res_f2 = open('./result/order4.txt', 'w')
    for x in res:
        res_f2.write(str(x) + ' ')
    res_f2.close()


if __name__ == "__main__":
    main()
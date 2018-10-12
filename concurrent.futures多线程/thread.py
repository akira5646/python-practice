from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

def pr(n):
    print(n)
    return "输出"+str(n)

if __name__ == '__main__':
    
    with ThreadPoolExecutor(max_workers=15) as threadpool:
        # 多线程执行函数pr(n),map有序
        all_task=threadpool.map(pr,range(1,100))
        # print(list(all_task))
        for result in all_task:
            print(result)

        # 多线程执行函数pr(n),submit无序
        all_task=[threadpool.submit(pr,n) for n in range(1,100)]
        for futures in as_completed(all_task):
            result = futures.result()
            print(result)
        
        
        
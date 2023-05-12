import time
from workers.SleepyWorkers import SleepyWorker
from workers.SquaredSumWorkers import SquaredSumWorker


def main(): #with threading
    calc_start_time = time.time()

    current_threads = []
    for i in range(5): #create 5 threads
        maximum_value = (i+1) * 100000
        squaredsumworkers = SquaredSumWorker(n=maximum_value)
        current_threads.append(squaredsumworkers)
    
    for i in range(len(current_threads)):
        current_threads[i].join()

    print("\n"+'Calculate sum of square took: ', time.time() - calc_start_time)


    sleep_start_time = time.time()

    current_threads = []
    for seconds in range(1,6): #create 5 threads
        sleepyWorker = SleepyWorker(seconds=seconds, daemon = True)
        current_threads.append(sleepyWorker) #thread execure after each


    # for i in range(len(current_threads)):#check if previous thread completed
    #     current_threads[i].join()
    
    print('Sleep took: ',time.time() - sleep_start_time)

if __name__ == "__main__":
    main()
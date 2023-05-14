import asyncio #1 core and 1 thread #threading 1 core and many threads
import time
#async in loops
async def async_sleep(n):  # couroutine
    print('Before sleep',n)
    for i in range(1,n):
        yield i
        await asyncio.sleep(i) # while sleeping execute another/next couroutine
    print('After sleep',n)

async def print_hello():
    print('hello')

async def main():
    start_time = time.time()
    async for k in async_sleep(5): #sequential loop
        print(k)
    print('totaltime:', time.time() - start_time)

if __name__ == '__main__':
    asyncio.run(main())

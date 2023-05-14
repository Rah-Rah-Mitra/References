import asyncio #1 core and 1 thread #threading 1 core and many threads
import time

async def async_sleep(n):  # couroutine
    print('Before sleep',n)
    await asyncio.sleep(n) # while sleeping execute another/next couroutine
    print('After sleep',n)

async def print_hello():
    print('hello')

async def main():
    start_time = time.time()
    await asyncio.gather(async_sleep(1), async_sleep(2), print_hello())
    print('totaltime:', time.time() - start_time)

if __name__ == '__main__':
    asyncio.run(main())

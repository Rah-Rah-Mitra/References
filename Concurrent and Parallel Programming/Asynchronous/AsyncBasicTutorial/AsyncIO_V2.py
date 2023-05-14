import asyncio #sequential so far
import time

async def async_sleep(n):  # couroutine
    print('Before sleep',n)
    await asyncio.sleep(5)
    print('After sleep',n)

async def print_hello():
    print('hello')

async def main():
    start_time = time.time()
    task = asyncio.create_task(async_sleep(1)) 
    await async_sleep(2) #running simultaniously order of execution 1st            
    await task          #running simultaniously order of execution 2nd
    await print_hello()
    print('totaltime:', time.time() - start_time)

if __name__ == '__main__':
    asyncio.run(main())

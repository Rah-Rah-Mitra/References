import asyncio  # sequential so far


async def async_sleep():  # couroutine
    print('Before sleep')
    await asyncio.sleep(5)
    print('After sleep')


async def print_hello():
    print('hello')


async def return_hello():
    return 'hello returned'


async def main():
    await async_sleep()  # blocker
    await print_hello()
    result = await return_hello()
    print(result)

if __name__ == '__main__':
    asyncio.run(main())

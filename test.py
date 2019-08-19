# coding=utf-8

import asyncio
import requests
import random
import threading



import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
import time

url = "http://127.0.0.1:5000"

loop = asyncio.get_event_loop()


async def cor():
    print("c-start")
    await asyncio.sleep(4)
    print("c-end")


async def main():
    tasks = [loop.create_task(cor()) for _ in range(10)]
    print("finish tasks======")
    for i, task in enumerate(tasks):
        print("start", i)
        time.sleep(5)
        await task
        print("end", i)

loop.run_until_complete(main())

adfads

pool = ThreadPoolExecutor(20)



def request(i):
    print("start", i)
    time.sleep(5)
    text = requests.get(url).text
    print("content:", i,  text)
    print(threading.get_ident())
    return text


# f0 = loop.run_in_executor(pool, request)
# f1 = loop.run_in_executor(pool, request)
# futures = [loop.run_in_executor(pool, request, i) for i in range(20)]
# futures = [loop.run_in_executor(None, requests.get, "http://127.0.0.1:5000") for _ in range(10)]
# print("======")


async def cor(i):
    for j in range(20):
        future = loop.run_in_executor(pool, request, "{}_{}".format(i, j))
        await future
        print("cor", i)
    print("end-cor", i)

loop.run_until_complete(asyncio.gather(*[cor(i) for i in range(10)]))


# async def main():
#     # for future in futures:
#     for i in range(10):
#         # future = loop.run_in_executor(pool, request)
#         await futures[i]
#         print("end", i)
#
# loop.run_until_complete(main())

# async def test():
#     print("start")
#     # await asyncio.sleep(2)
#     request_future = loop.run_in_executor(pool, request)
#     result = await request_future
#     print("end")
#
#
#
#
# async def main():
#     tasks = [loop.create_task(test()) for _ in range(10)]
#     for i in range(10):
#         await tasks[i]
#         print("task end", i)
#
#
# loop.run_until_complete(main())
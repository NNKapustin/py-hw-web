import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        # response = await session.post(
        #     "http://127.0.0.1:8080/user/",
        #     json={"name": "user_2", "password": '1234'}
        # )
        # data = await response.json()
        # print(data)
        # response = await session.get(
        #     "http://127.0.0.1:8080/user/1/",
        #
        # )
        # data = await response.json()
        # print(data)

        # response = await session.patch(
        #     "http://127.0.0.1:8080/user/1/",
        #     json={"name": "user_3"}
        # )
        # data = await response.json()
        # print(data)
        #
        # response = await session.get(
        #     "http://127.0.0.1:8080/user/1/",
        #
        # )
        # data = await response.json()
        # print(data)

        response = await session.delete(
            "http://127.0.0.1:8080/user/1/",
        )
        data = await response.json()
        print(data)

        response = await session.get(
            "http://127.0.0.1:8080/user/1/",

        )
        data = await response.json()
        print(data)


asyncio.run(main())

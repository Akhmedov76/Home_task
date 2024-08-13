import aiohttp
import asyncio


async def print_hello():
    for _ in range(10):
        print("hello")
        await asyncio.sleep(0.1)


async def get_cat_facts():
    url = "https://cat-fact.herokuapp.com/facts"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            facts = [fact['text'] for fact in data][:20]
            return facts


async def cat_fact_generator():
    url = "https://cat-fact.herokuapp.com/facts"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            for fact in data[:20]:
                yield fact['text']


async def filter_fact(fact):
    if len(fact) > 100:
        return fact
    return None


async def main():
    facts_task = asyncio.create_task(get_cat_facts())
    hello_task = asyncio.create_task(print_hello())

    facts = await facts_task
    await hello_task

    print("\n20 info about cats:")
    for fact in facts:
        print(fact)

    print("\nGenerator info  about cats:")
    async for fact in cat_fact_generator():
        filtered_fact = await filter_fact(fact)
        if filtered_fact:
            print(filtered_fact)

asyncio.run(main())

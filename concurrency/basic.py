import asyncio
from itertools import cycle
import random

async def mygen(u: int = 10):
    """Yield powers of 2."""
    i = 0
    while i < u:
        yield 2 ** i
        i += 1
        await asyncio.sleep(0.1)

async def main():
    # This does *not* introduce concurrent execution
    # It is meant to show syntax only
    g = [i async for i in mygen()]
    f = [j async for j in mygen() if not (j // 3 % 5)]
    print(g, f)

if __name__=='__main__':

	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
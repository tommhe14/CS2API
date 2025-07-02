from cs2api import CS2

import asyncio
import json

cs2 = CS2()

async def test():
    testRequest = await cs2.get_player_transfers(31349)
    print(json.dumps(testRequest, indent = 4))
    await cs2.close()

asyncio.run(test())
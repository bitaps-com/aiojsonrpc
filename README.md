# aiojsonrpc
Python asyncio client interface fo JSON-RPC 2.0


#### Example

```angular2html
import asyncio
import aiojsonrpc

async def test(loop):
    t = aiojsonrpc.rpc("http://user:password@host:port", loop)
    while 1:
        p = await  t.getinfo()
        print(p)
        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.create_task(test(loop))
loop.run_forever()
```

```angular2html
python3 test.py 
{'timeoffset': 0, 'version': 140200, 'relayfee': 1e-05, 'connections': 18, 'difficulty': 708659466230.332, 'proxy': '', 'testnet': False, 'errors': '', 'blocks': 475003, 'protocolversion': 70015}

```

```angular2html
import asyncio
import aiojsonrpc

async def test(loop):
    t = aiojsonrpc.rpc("http://user:password@host:port  ", loop)
    while 1:
        p = await t.batch([["net_peerCount"],
                           ["net_peerCount"],
                           ["eth_getTransactionByHash",
                            "0xbcad8332d6d68344389f69ec547ecea4a838a2a2cab50407cf7d082531a7c058"]])
        print(p)
        await asyncio.sleep(10)

loop = asyncio.get_event_loop()
loop.create_task(test(loop))
loop.run_forever()

```

```angular2html
python3 test.py 
[{'jsonrpc': '2.0', 'id': 1, 'result': '0x19'}, {'jsonrpc': '2.0', 'id': 2, 'result': '0x19'}, {'jsonrpc': '2.0', 'id': 3, 'result': None}]

```

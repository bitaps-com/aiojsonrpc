# aiojsonrpc
Python asyncio interface fo JSON-RPC API


#### Example

```
import asyncio
import aiojsonrpc

async def test(loop):
    try:
        t = aiojsonrpc.rpc("http://user:password@host:port", loop)
        while 1:
            p = await  t.getinfo()
            print(p)
            await asyncio.sleep(10)
    except:
        import traceback
        print(traceback.format_exc())

loop = asyncio.get_event_loop()
loop.create_task(test(loop))
loop.run_forever()
```

```
python3 test.py 
{'timeoffset': 0, 'version': 140200, 'relayfee': 1e-05, 'connections': 18, 'difficulty': 708659466230.332, 'proxy': '', 'testnet': False, 'errors': '', 'blocks': 475003, 'protocolversion': 70015}

```

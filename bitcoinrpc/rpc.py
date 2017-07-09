import aiohttp
import json



class JSONRPCException(Exception):
    def __init__(self, rpc_error):
        parent_args = []
        try:
            parent_args.append(rpc_error['message'])
        except:
            pass
        Exception.__init__(self, *parent_args)
        self.error = rpc_error
        self.code = rpc_error['code'] if 'code' in rpc_error else None
        self.message = rpc_error['message'] if 'message' in rpc_error else None

    def __str__(self):
        return '%d: %s' % (self.code, self.message)

    def __repr__(self):
        return '<%s \'%s\'>' % (self.__class__.__name__, self)



HTTP_TIMEOUT = 30

class AIOJSONRPC(object):
    __request_id = 0

    def __init__(self, url, loop,
                 method = None, timeout = HTTP_TIMEOUT,
                 session = None ):
        if session is None:
            self.__session = aiohttp.ClientSession()
        else:
            self.__session = session
        self.__loop = loop
        self.__timeout = timeout
        self.__method = method
        self.__url = url



    def __call__(self, *args):
        AIOJSONRPC.__request_id += 1
        p = self.__loop.create_task(self.__request(self.__method, AIOJSONRPC.__request_id, args))
        return p


    async def __request(self, method, id, args):
        post = json.dumps({'version': '2.0',
                               'method': self.__method,
                               'params': args,
                               'id': AIOJSONRPC.__request_id})
        async with self.__session.post(self.__url, data=post, timeout = self.__timeout) as response:
            response = await self.handle_response(response)
            if response.get('error') is not None:
                raise JSONRPCException(response['error'])
            elif 'result' not in response:
                raise JSONRPCException({
                    'code': -343, 'message': 'missing JSON-RPC result'})
        return response['result']

    async def handle_response(self, response):
        if response is None:
            raise JSONRPCException({
                'code': -342, 'message': 'missing HTTP response from server'})
        try:
            assert response.headers["Content-type"] == 'application/json'
        except Exception:
            raise JSONRPCException({
                'code': -342, 'message': 'non-JSON HTTP response with \'%i %s\' from server' %
                                   (response.status, response.reason)})
        try:
            text = await response.text()
            response = json.loads(text)
        except Exception:
            raise JSONRPCException({
                'code': -342, 'message': 'decode JSON response error'})
        return response


    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError
        return AIOJSONRPC(self.__url,
                          self.__loop, name, self.__timeout, self.__session)



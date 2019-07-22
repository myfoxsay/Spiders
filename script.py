from mitmproxy import ctx
def request(flow):
    flow.request.headers['User-Agent']='MitmProxy'
    #print(flow.request.headers)
    #ctx.log.info(str(flow.request.headers))
    #ctx.log.warn(str(flow.request.headers))
    #ctx.log.error(str(flow.request.headers))
def response(flow):
    print(flow.request.url)
    print(flow.response.text)


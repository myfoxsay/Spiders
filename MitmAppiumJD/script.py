import json
import pymongo
from urllib.parse import unquote
import re

import collections
import random
from enum import Enum
import json

import mitmproxy
from mitmproxy import ctx
from mitmproxy.exceptions import TlsProtocolException
from mitmproxy.proxy.protocol import TlsLayer, RawTCPLayer


#client = pymongo.MongoClient('localhost')

class Listener:
    def __init__(self):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['jd']
        self.comments_collection = db['comments']
        self.products_collection = db['products']

    def response(self,flow):
        #global comments_collection, products_collection
        # 提取评论数据
        url = 'api.m.jd.com/client.action'
        if url in flow.request.url:
            pattern = re.compile('sku\".*?\"(\d+)\"')
            # Request请求参数中包含商品ID
            body = unquote(flow.request.text)
            # 提取商品ID
            id = re.search(pattern, body).group(1) if re.search(pattern, body) else None
            # 提取Response Body
            text = flow.response.text
            data = json.loads(text)
            comments = data.get('commentInfoList') or []
            # 提取评论数据
            for comment in comments:
                if comment.get('commentInfo') and comment.get('commentInfo').get('commentData'):
                    info = comment.get('commentInfo')
                    text = info.get('commentData')
                    date = info.get('commentDate')
                    nickname = info.get('userNickName')
                    pictures = info.get('pictureInfoList')
                    print(id, nickname, text, date)
                    self.comments_collection.insert({
                        'id': id,
                        'text': text,
                        'date': date,
                        'nickname': nickname,
                        'pictures': pictures
                    })

        url = 'cdnware.m.jd.com'
        if url in flow.request.url:
            text = flow.response.text
            data = json.loads(text)
            if data.get('wareInfo') and data.get('wareInfo').get('basicInfo'):
                info = data.get('wareInfo').get('basicInfo')
                id = info.get('wareId')
                name = info.get('name')
                images = info.get('wareImage')
                print(id, name, images)
                self.products_collection.insert({
                    'id': id,
                    'name': name,
                    'images': images
                })
addons=[
    Listener()
]


#以下代码直接拷贝即可
class InterceptionResult(Enum):
    success = True
    failure = False
    skipped = None


class _TlsStrategy:
    """
    Abstract base class for interception strategies.
    """

    def __init__(self):
        # A server_address -> interception results mapping
        self.history = collections.defaultdict(lambda: collections.deque(maxlen=500))

    def should_intercept(self, server_address):
        """
        Returns:
            True, if we should attempt to intercept the connection.
            False, if we want to employ pass-through instead.
        """
        raise NotImplementedError()

    def record_success(self, server_address):
        self.history[server_address].append(InterceptionResult.success)

    def record_failure(self, server_address):
        self.history[server_address].append(InterceptionResult.failure)

    def record_skipped(self, server_address):
        self.history[server_address].append(InterceptionResult.skipped)


class ConservativeStrategy(_TlsStrategy):
    """
    Conservative Interception Strategy - only intercept if there haven't been any failed attempts
    in the history.
    """

    def should_intercept(self, server_address):
        if InterceptionResult.failure in self.history[server_address]:
            return False
        return True


class ProbabilisticStrategy(_TlsStrategy):
    """
    Fixed probability that we intercept a given connection.
    """

    def __init__(self, p):
        self.p = p
        super(ProbabilisticStrategy, self).__init__()

    def should_intercept(self, server_address):
        return random.uniform(0, 1) < self.p


class TlsFeedback(TlsLayer):
    """
    Monkey-patch _establish_tls_with_client to get feedback if TLS could be established
    successfully on the client connection (which may fail due to cert pinning).
    """

    def _establish_tls_with_client(self):
        server_address = self.server_conn.address

        try:
            super(TlsFeedback, self)._establish_tls_with_client()
        except TlsProtocolException as e:
            tls_strategy.record_failure(server_address)
            raise e
        else:
            tls_strategy.record_success(server_address)


# inline script hooks below.

tls_strategy = None


def load(l):
    l.add_option(
        "tlsstrat", int, 0, "TLS passthrough strategy (0-100)",
    )


def configure(updated):


    global tls_strategy
    if ctx.options.tlsstrat > 0:
        tls_strategy = ProbabilisticStrategy(float(ctx.options.tlsstrat) / 100.0)
    else:
        tls_strategy = ConservativeStrategy()


def next_layer(next_layer):
    """
    This hook does the actual magic - if the next layer is planned to be a TLS layer,
    we check if we want to enter pass-through mode instead.
    """
    if isinstance(next_layer, TlsLayer) and next_layer._client_tls:
        server_address = next_layer.server_conn.address

        if tls_strategy.should_intercept(server_address):
            # We try to intercept.
            # Monkey-Patch the layer to get feedback from the TLSLayer if interception worked.
            next_layer.__class__ = TlsFeedback
        else:
            # We don't intercept - reply with a pass-through layer and add a "skipped" entry.
            mitmproxy.ctx.log("TLS passthrough for %s" % repr(next_layer.server_conn.address), "info")
            next_layer_replacement = RawTCPLayer(next_layer.ctx, ignore=True)
            next_layer.reply.send(next_layer_replacement)
            tls_strategy.record_skipped(server_address)
# -*- coding: utf-8 -*-
from concurrent import futures
import grpc
import time
import sys
sys.path.append("./rpc")


from GoogleFreeTrans import Translator
from rpc import rpc_methods_pb2, rpc_methods_pb2_grpc

import parsel
import urllib.request
from functools import reduce

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8972'


def getSentence(content):
    textList = []
    sentence = ""
    for x in content:
        y = '\{}'.format(x)
        z = eval('u"%s"' % y)
        textList.append(z)

        if len(textList) == 3:
            try:
                string = reduce(lambda x, y: x + y, textList).encode('raw_unicode_escape').decode()
            except BaseException as Argument:
                print("UnicodeDecodeError:", Argument)
            else:
                sentence += string
                textList.clear()

    return sentence


def visitURL(base_url):
    # base_url = "https://mp.weixin.qq.com/s?src=11&timestamp=1586779202&ver=2276&signature=Hu*YxuJwLetW6Eu24Hju2QRQyiQten3BK8ER9i92SnqBja57Pbn*MLtAb8XEMKpPs0nLxl8IU3T6TRck1EGWlPYLfGBBy8pKPXKqSeHv-Oc=&new=1"

    html = urllib.request.urlopen(base_url).read()
    data = parsel.Selector(str(html))
    text = data.xpath('//div[@class="rich_media_content "]/p/text()').extract()
    if not text:
        print("None,change filter2")
        text = data.xpath('//section[@data-bcless="lighten"]//span/text()').extract()

    if not text:
        print("None,change filter3")
        text = data.xpath('//div[@class="rich_media_content "]//section/text()').extract()

    if not text:
        print("None,change filter4")
        text = data.xpath('//div[@class="rich_media_content "]/text()').extract()

    translator = Translator.translator(src='zh-CN', dest='en')

    page_content = ""
    if not text:
        print("empty response")
        return page_content

    for item in text:
        text_split = item.split('\\')[1:]

        raw_paper_sentence = getSentence(text_split)
        transed_paper_sentence = translator.translate(raw_paper_sentence)
        # print(raw_paper_sentence+'\n'+transed_paper_sentence)

        page_content += transed_paper_sentence

    return page_content


class GetSearch(rpc_methods_pb2_grpc.GetSearchServicer):
    def SearchInfo(self, request, context):
        print("\n开始爬取：", request.url)
        response = visitURL(request.url)
        if not response:
            response = "爬取失败"
        length = 0
        if len(response)>30:
            length = 30
        else:
            length = len(response)
        print("爬取结果："+response[:length]+"……")
        return rpc_methods_pb2.Res(res=response)


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpc_methods_pb2_grpc.add_GetSearchServicer_to_server(GetSearch(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    print("[start listen] " + _HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    serve()

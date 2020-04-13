#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from concurrent import futures
import rpc_methods_pb2,rpc_methods_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8972'


import json
import wechatsogou
from wechatsogou.const import WechatSogouConst

# 直连
ws_api = wechatsogou.WechatSogouAPI()

# searchName = '牛羊天地'
# res = ws_api.search_article(searchName,1,WechatSogouConst.search_article_time.day)
# for item in res:
#     json_item = json.dumps(item)
#     print(json_item)
#     print("\n\n")




class GetSearch(rpc_methods_pb2_grpc.GetSearchServicer):
    print("cls")
    def SearchInfo(self, request, context):
        res = ws_api.search_article(request.keyword,request.page,WechatSogouConst.search_article_time.day)
        json_res  = ""
        for item in res:
            json_item = json.dumps(item)
            # print(json_item)
            json_res = json_res + json_item
        # print("fct:",request)
        return rpc_methods_pb2.Res(res=json_res)

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpc_methods_pb2_grpc.add_GetSearchServicer_to_server(GetSearch(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()
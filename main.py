import json

import brotli as brotli
import websocket

from test import encode_data
from test import convert_to_object
import requests

def get_danmuku():
    h = {
        'Cookie': "",
    }
    res = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo?id=23167843&type=0', headers=h).json()
    print(res)

def open(ws):
    # ccokie模式 可以显示用户全部消息
    data = {"uid":3537111630219964,"roomid":23167843,"protover":3,"buvid":"","platform":"web","type":2,"key":"zcpOrDOlpuL0e-QmaF5jZYeqsAb7fh-9nC9XqVrU8i0QR2F5sW-JvDKXmJg8aJV2pOO1mQprD7_h8G26hwQQHa_q37OjyN01gRfTTp0HDGtMQ4MIuLBDja2vNg-6UIoaHY2N9E7t58K8c-_mBRCw5F3gqGIi1xg="}
    # 非cookie模式 用户昵称会加密
    # data = {"uid": 0,"roomid":23167843,"protover":3,"buvid":"","platform":"web","type":2,"key":"OOW1Y7U0hukdvUbKkEvsxOTQdo18IZ96ofi5I8ZKdwyAIrWlqbIORm6Fy4j8Q3-rEN2aNm04bxjCSvJudPPU9RzthqN0DnDMM9MOglJhCcXXOfrZom7V3GQ47zikxU4tfe91wVwnyXFqtWT7TA=="}
    data = json.dumps(data)
    # print(data)
    ws.send(encode_data(data, 7), websocket.ABNF.OPCODE_BINARY)
    ws.send(encode_data("{}", 2), websocket.ABNF.OPCODE_BINARY)
def message(ws,data):

    data = convert_to_object(data)

    if isinstance(data['body'], list):
        for sub_body in data['body']:
            # print(sub_body)
            if isinstance(sub_body, list):
                for sub_item in sub_body:
                    # pass
                    # print(sub_item)
                    # ['cmd', 'info', 'dm_v2']
                    print(sub_item['cmd'])
                    # continue
                    # 进入直播间
                    if sub_item['cmd'] == 'INTERACT_WORD':
                        print(sub_item)
                    continue
                    # 弹幕
                    if sub_item['cmd'] == 'DANMU_MSG':
                        # print(len(sub_item['info']))
                        # 弹幕内容是1
                        # print(sub_item['info'][1])
                        # print(sub_item['info'][2])
                        # print(sub_item['info'][3])
                        # print(sub_item['info'][4])
                        for info in sub_item['info']:
                            print(info)
                        #     print("======")
                        #     print(info[0])
                        print("------")
                continue
            # print(sub_body)
        return
    # print(data)


    # print(decompressed_data)
def error(ws, data):
    print(data)

def close(ws, err, a):
    print(err)
    print(a)

if __name__ == '__main__':
    # url = "wss://cn-sdqd-ccc-live-tracker-01.chat.bilibili.com/?protocol=10&stream=live_630455196_44327268_1500&roomid=23167843&timeshift=0"
    get_danmuku()
    # url = 'wss://tx-bj-live-comet-10.chat.bilibili.com/sub'
    # h = {
    #     'cookie': "buvid3=498A93D9-462A-9C6B-6D8A-E4C12100A30C32999infoc; b_nut=1673718632; i-wanna-go-back=-1; _uuid=10579DEA3-E83B-EB32-10E15-3617D1E2672B34690infoc; buvid4=E51A7F6E-7EAE-5668-4BE4-DED9358D140B07517-022052015-p7UKSeFfDyU2xNNunqTBEQ%3D%3D; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(J~lu|m~|)u0J'uY~J~u)Y~k; buvid_fp_plain=undefined; b_ut=5; header_theme_version=CLOSE; FEED_LIVE_VERSION=V8; LIVE_BUVID=AUTO4216850228969239; fingerprint=a073d84e328389b11f52f8a28ca15c6f; buvid_fp=a073d84e328389b11f52f8a28ca15c6f; DedeUserID=3537111630219964; DedeUserID__ckMd5=5e53be21700404c6; home_feed_column=5; browser_resolution=1440-695; bp_video_offset_3537111630219964=0; innersign=0; b_lsid=D93751C7_18AA275CB3E; SESSDATA=db955027%2C1710494744%2Cbc563%2A92CjAMCP0AnqSVzwT7H-KW7X6etzQOoElo-lwWsU_PMH0EHLrr83fjqiSnu2GVmMO_fbQSVjBIZm9FdGhoNDhURTVWXzRKaDVUaW1EN1JsVENTcTBpRmFyN1lYTERNbXZ2QTFaR3k0b1dnUzYwQl8zSVNVeWJGalA4TzZFLTNuRGYyUlFPc2I1QzBBIIEC; bili_jct=b577081a31606753d4061bef8d338d55; sid=pe6o2vnk; PVID=4",
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    # }
    # ws = websocket.WebSocketApp(url, on_open=open, on_message=message, on_close=close, on_error=error, header=h)
    # ws.run_forever()
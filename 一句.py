from xiaoai import *
import requests
import random


def outputJson(toSpeakText, is_session_end, openMic=True):
    xiaoAIResponse = XiaoAIResponse(to_speak=XiaoAIToSpeak(type_=0, text=toSpeakText), open_mic=openMic)
    response = xiaoai_response(XiaoAIOpenResponse(version="1.0",
                                                  is_session_end=is_session_end,
                                                  response=xiaoAIResponse))
    return response


def main(event):
    req = xiaoai_request(event)
    url2='https://v1.hitokoto.cn/?c='
    x1=requests.get(url='https://v1.hitokoto.cn/')
    x1 = x1.json()['hitokoto']+'  来自'+x1.json()['from']
    if req.request.type == 0:
        return outputJson(x1, False)
    elif req.request.type == 1:
        if ((not hasattr(req.request, "slot_info")) or (not hasattr(req.request.slot_info, "intent_name"))):
            return outputJson("抱歉，我没有听懂,您可以说再来一句,也可以说来一句英语或者其他", False)
        else:
            if req.request.slot_info.intent_name == 'get':
                slotsList = req.request.slot_info.slots
                # 提问时根据类型查询api并返回
                for item in slotsList:
                    if item['name'] == 'b':
                        l1 = [item]
                        t1 = l1[0].get('value', "")
                        if t1=='英语':
                            # 英语使用了另一个api,需要构造随机日期来获得句子
                            a=str(random.randint(2013,2017))
                            b=str(random.randint(1,12))
                            c=str(random.randint(1,29))
                            url1='http://open.iciba.com/dsapi/?date='+a+'-'+b+'-'+c
                            x2 = requests.get(url=url1)
                            x2= x2.json()['content']+x2.json()['note']
                            return outputJson(x2, False)
                        elif t1=='动画':
                            url2=url2+'a'
                            x3 = requests.get(url=url2)
                            x3 = x3.json()['hitokoto'] + '  来自' + x3.json()['from']
                            return outputJson(x3, False)
                        elif t1=='动漫':
                            url2=url2+'b'
                            x3 = requests.get(url=url2)
                            x3 = x3.json()['hitokoto'] + '  来自' + x3.json()['from']
                            return outputJson(x3, False)
                        elif t1=='游戏':
                            url2=url2+'c'
                            x3 = requests.get(url=url2)
                            x3 = x3.json()['hitokoto'] + '  来自' + x3.json()['from']
                            return outputJson(x3, False)
                        elif t1=='小说':
                            url2=url2+'d'
                            x3 = requests.get(url=url2)
                            x3 = x3.json()['hitokoto'] + '  来自' + x3.json()['from']
                            return outputJson(x3, False)
                        elif t1=='原创':
                            url2=url2+'e'
                            x3 = requests.get(url=url2)
                            x3 = x3.json()['hitokoto'] + '  来自' + x3.json()['from']
                            return outputJson(x3, False)
                    return outputJson(x1, False)
            else:
                return outputJson("抱歉，我没有听懂,您可以说再来一句,也可以说来一句英语", False)
    else:
        return outputJson("一句和您下次再见", True, False)
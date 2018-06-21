from xiaoai import *
import requests
import time
def outputJson(toSpeakText, is_session_end, openMic=True):
    xiaoAIResponse = XiaoAIResponse(to_speak=XiaoAIToSpeak(type_=0, text=toSpeakText), open_mic=openMic)
    response = xiaoai_response(XiaoAIOpenResponse(version="1.0",
                                                  is_session_end=is_session_end,
                                                  response=xiaoAIResponse))
    return response
def main(event):
    req = xiaoai_request(event)
    if req.request.type == 0:
        return outputJson("请问你想要去哪里", False)
    elif req.request.type == 1:
        if ((not hasattr(req.request, "slot_info")) or (not hasattr(req.request.slot_info, "intent_name"))):
            return outputJson("抱歉，我没有听懂", False)
        else:
            if req.request.slot_info.intent_name == 'get':
                slotsList = req.request.slot_info.slots
                list1 = [item for item in slotsList if item['name'] == 'a']
                name = str(list1[0].get('value', ""))
                t0=time.time()
                # 下面是获取到景点ID
                url1 = 'http://api01.bitspaceman.com:8000/sight/tripadvisor?apikey=EefogiOK4adJ3LAQBI1uFqtvJJc06U2KsEZ3tevOEMy5yOd88AfEk2fmruH9Ibo4&kw=' + name
                headers = {"Accept-Encoding": "gzip", "Connection": "close"}
                x1 = requests.get(url=url1, headers=headers)
                id = x1.json()['data'][0]['id']
                # 最后也没能解决超时技能自动退出问题
                if time.time() - t0 > 2:  # 经常超时没办法
                    return outputJson("抱歉，请再试一次", False)
                # 下面是获得景点评论
                url2 = 'http://120.76.205.241:8000/comment/tripadvisor?type=1&apikey=EefogiOK4adJ3LAQBI1uFqtvJJc06U2KsEZ3tevOEMy5yOd88AfEk2fmruH9Ibo4&id=' + id
                x2 = requests.get(url=url2, headers=headers)
                comment = x2.json()['data'][0]['content']
                return outputJson(comment,True, False)
            else:
                return outputJson("抱歉，我没有听懂", False)
    else:
        return outputJson("", False)
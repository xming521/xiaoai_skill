from xiaoai import *
import requests

def outputJson(toSpeakText, is_session_end, openMic=True):
    xiaoAIResponse = XiaoAIResponse(to_speak=XiaoAIToSpeak(type_=0, text=toSpeakText), open_mic=openMic)
    response = xiaoai_response(XiaoAIOpenResponse(version="1.0",
                                                  is_session_end=is_session_end,
                                                  response=xiaoAIResponse))
    return response

def main(event):
    #下面地址不一样  自制的小东西
    x = requests.get(url='http://58.87.66.50/weak.txt')
    x.encoding = 'gbk'
    x=x.text.replace('\r','')

    req = xiaoai_request(event)
    if req.request.type == 0:
        return outputJson(x,True,False)
    elif req.request.type == 1:
        if ((not hasattr(req.request, "slot_info")) or (not hasattr(req.request.slot_info, "intent_name"))):
            return outputJson("抱歉，我没有听懂", False)
        else:
            if req.request.slot_info.intent_name == 'num':
                slotsList = req.request.slot_info.slots
                num = [item for item in slotsList if item['name'] == 'n']

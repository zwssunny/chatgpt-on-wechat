# encoding:utf-8

import json
import uuid
import requests
from common.log import logger
from bot.bot import Bot
from config import conf
from uuid import getnode as get_mac

# Baidu Unit对话接口 (可用, 但能力较弱)


class BaiduUnitBot(Bot):
    """
    在https://ai.baidu.com/unit/v2#/myrobot 里注册创建一个机器人
    得到一个机器人 ID ，
    然后访问下面页面获取 API Key 和 Secret Key：
    https://console.bce.baidu.com/ai
    请在config.json增加配置参数:
    "baiduunit": {
        "service_id": "s...", #机器人编号
        "api_key": "",
        "secret_key": ""
        }
    """

    def __init__(self):
        self.access_token = self.get_token()

    def reply(self, query, context=None):
        # token = self.access_token
        # url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=' + token
        # post_data = "{\"version\":\"3.0\",\"service_id\":\"S73177\",\"session_id\":\"\",\"log_id\":\"7758521\",\"skill_ids\":[\"1221886\"],\"request\":{\"terminal_id\":\"88888\",\"query\":\"" + query + "\", \"hyper_params\": {\"chat_custom_bot_profile\": 1}}}"
        # print(post_data)
        # headers = {'content-type': 'application/x-www-form-urlencoded'}
        # response = requests.post(url, data=post_data.encode(), headers=headers)
        # if response:
        #     return response.json()['result']['context']['SYS_PRESUMED_HIST'][1]

        return self.getSay(query)

    def get_token(self):
        """获取访问百度UUNIT 的access_token
        #param api_key: UNIT apk_key
        #param secret_key: UNIT secret_key
        Returns:
            string: access_token
        """        
        api_key = conf()["baiduunit"].get("api_key")
        secret_key = conf()["baiduunit"].get("secret_key")
        url = "https://aip.baidubce.com/oauth/2.0/token?client_id={}&client_secret={}&grant_type=client_credentials".format(
            api_key, secret_key)
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        return response.json()['access_token']

    def getUnit(self, query):
        """
        NLU 解析version 3.0
        :param query: 用户的指令字符串
        :returns: UNIT 解析结果。如果解析失败，返回 None
        """
        service_id = conf()["baiduunit"].get("service_id")
        
        url = (
            'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token='
            + self.access_token
        )
        request = {"query": query, "user_id": str(
            get_mac())[:32], "terminal_id": "88888"}
        body = {
            "log_id": str(uuid.uuid1()),
            "version": "3.0",
            "service_id": service_id,
            "session_id": str(uuid.uuid1()),
            "request": request,
        }
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=body, headers=headers)
            return json.loads(response.text)
        except Exception:
            return None

    def getUnit2(self, query):
        """
        NLU 解析 version 2.0

        :param query: 用户的指令字符串
        :returns: UNIT 解析结果。如果解析失败，返回 None
        """
        service_id = conf()["baiduunit"].get("service_id")
        # access_token = self.get_token()
        url = (
            "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token="
            + self.access_token
        )
        request = {"query": query, "user_id": str(get_mac())[:32]}
        body = {
            "log_id": str(uuid.uuid1()),
            "version": "2.0",
            "service_id": service_id,
            "session_id": str(uuid.uuid1()),
            "request": request,
        }
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=body, headers=headers)
            return json.loads(response.text)
        except Exception:
            return None

    def getIntent(self, parsed):
        """
        提取意图

        :param parsed: UNIT 解析结果
        :returns: 意图数组
        """
        if (
            parsed
            and "result" in parsed
            and "response_list" in parsed["result"]
        ):
            try:
                return parsed["result"]["response_list"][0]["schema"]["intent"]
            except Exception as e:
                logger.warning(e)
                return ""
        else:
            return ""

    def hasIntent(self, parsed, intent):
        """
        判断是否包含某个意图

        :param parsed: UNIT 解析结果
        :param intent: 意图的名称
        :returns: True: 包含; False: 不包含
        """
        if (
            parsed
            and "result" in parsed
            and "response_list" in parsed["result"]
        ):
            response_list = parsed["result"]["response_list"]
            for response in response_list:
                if (
                    "schema" in response
                    and "intent" in response["schema"]
                    and response["schema"]["intent"] == intent
                ):
                    return True
            return False
        else:
            return False

    def getSlots(self, parsed, intent=""):
        """
            提取某个意图的所有词槽

            :param parsed: UNIT 解析结果
            :param intent: 意图的名称
            :returns: 词槽列表。你可以通过 name 属性筛选词槽，
        再通过 normalized_word 属性取出相应的值
        """
        if (
            parsed
            and "result" in parsed
            and "response_list" in parsed["result"]
        ):
            response_list = parsed["result"]["response_list"]
            if intent == "":
                try:
                    return parsed["result"]["response_list"][0]["schema"]["slots"]
                except Exception as e:
                    logger.warning(e)
                    return []
            for response in response_list:
                if (
                    "schema" in response
                    and "intent" in response["schema"]
                    and "slots" in response["schema"]
                    and response["schema"]["intent"] == intent
                ):
                    return response["schema"]["slots"]
            return []
        else:
            return []

    def getSlotWords(self, parsed, intent, name):
        """
        找出命中某个词槽的内容

        :param parsed: UNIT 解析结果
        :param intent: 意图的名称
        :param name: 词槽名
        :returns: 命中该词槽的值的列表。
        """
        slots = self.getSlots(parsed, intent)
        words = []
        for slot in slots:
            if slot["name"] == name:
                words.append(slot["normalized_word"])
        return words

    def getSayByConfidence(self, parsed):
        """
        提取 UNIT 置信度最高的回复文本

        :param parsed: UNIT 解析结果
        :returns: UNIT 的回复文本
        """
        if (
            parsed
            and "result" in parsed
            and "response_list" in parsed["result"]
        ):
            response_list = parsed["result"]["response_list"]
            answer = {}
            for response in response_list:
                if (
                    "schema" in response
                    and "intent_confidence" in response["schema"]
                    and (
                        not answer
                        or response["schema"]["intent_confidence"]
                        > answer["schema"]["intent_confidence"]
                    )
                ):
                    answer = response
            return answer["action_list"][0]["say"]
        else:
            return ""

    def getSay(self, parsed, intent=""):
        """
        提取 UNIT 的回复文本

        :param parsed: UNIT 解析结果
        :param intent: 意图的名称
        :returns: UNIT 的回复文本
        """
        if (
            parsed
            and "result" in parsed
            and "response_list" in parsed["result"]
        ):
            response_list = parsed["result"]["response_list"]
            if intent == "":
                try:
                    return response_list[0]["action_list"][0]["say"]
                except Exception as e:
                    logger.warning(e)
                    return ""
            for response in response_list:
                if (
                    "schema" in response
                    and "intent" in response["schema"]
                    and response["schema"]["intent"] == intent
                ):
                    try:
                        return response["action_list"][0]["say"]
                    except Exception as e:
                        logger.warning(e)
                        return ""
            return ""
        else:
            return ""

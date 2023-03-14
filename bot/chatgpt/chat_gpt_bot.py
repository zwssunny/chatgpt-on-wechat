# encoding:utf-8

import time
import threading
import openai

from bot.bot import Bot
from config import conf, load_config
from common.log import logger
from common.expired_dict import ExpiredDict
from common.messages_tokens import num_tokens_from_message
from bot.baidu.baidu_unit_bot import BaiduUnitBot


if conf().get('expires_in_seconds'):
    all_sessions = ExpiredDict(conf().get('expires_in_seconds'))
else:
    all_sessions = dict()

# OpenAI对话模型API (可用)


class ChatGPTBot(Bot):
    """
    OpenAIBot 自动对话机器人，继承于Bot

    Args:
        Bot (Bot): Auto-replay chat robot abstract class
    """

    def __init__(self):
        openai.api_key = conf().get('open_ai_api_key')
        proxy = conf().get('proxy')
        if proxy:
            openai.proxy = proxy
        baiduconfig = conf().get('baiduunit')
        if baiduconfig:
            self.baiduUnitBot = BaiduUnitBot()

    def reply(self, query, context=None):
        """
        acquire reply content

        Args:
            query (String): 用户询问内容
            context (String, optional): 询问类型(TEXT,IMAGE_CREATE). Defaults to None.

        Returns:
            String: 返回回复内容或者图片链接
        """
        if not context or not context.get('type') or context.get('type') == 'TEXT':
            logger.info("[OPEN_AI] query=%s", query)
            session_id = context.get(
                'session_id') or context.get('from_user_id')
            if query == '#清除记忆':
                Session.clear_session(session_id)
                return '记忆已清除'
            elif query == '#清除所有':
                Session.clear_all_session()
                return '所有人记忆已清除'
            elif query == '#更新配置':
                load_config()
                return '配置已更新'

            session = Session.build_session_query(query, session_id)
            logger.debug("[OPEN_AI] session query=%s", session)

            # 先调用百度机器人，如果能返回可以识别的意图，则返回结果，否则继续执行openai chat
            if self.baiduUnitBot:
                parsed = self.baiduUnitBot.getUnit2(query)
                intent = self.baiduUnitBot.getIntent(parsed)
                if intent:
                    logger.info("Baidu_AI Intent= %s", intent)
                    replytext = self.baiduUnitBot.getSay(parsed)
                    if replytext:
                        logger.info("Baidu_AI replytext= %s", replytext)
                        threading.Thread(target=Session.save_session, args=(
                            replytext, session_id, 0)).start()
                        return replytext

            # 找不到意图了，继续执行
            reply_content = self.reply_text(session, session_id, 0)
            logger.debug("[OPEN_AI] new_query=%s, user=%s, reply_cont=%s",
                         session, session_id, reply_content["content"])
            if reply_content["completion_tokens"] > 0:
                threading.Thread(target=Session.save_session, args=(
                    reply_content["content"], session_id, reply_content["total_tokens"])).start()
                # Session.save_session(reply_content["content"], session_id, reply_content["total_tokens"])
            return reply_content["content"]

        elif context.get('type', None) == 'IMAGE_CREATE':
            return self.create_img(query, 0)

    def reply_text(self, query, session_id, retry_count=0):
        '''
        call openai's ChatCompletion to get the answer
        :param query: query content
        :param session_id: from user id
        :param retry_count: retry count
        :return: Dictionary
        '''
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 对话模型的名称
                messages=query,
                temperature=0.9,  # 值在[0,1]之间，越大表示回复越具有不确定性
                # max_tokens=4096,  # 回复最大的字符数
                top_p=1,
                frequency_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                presence_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            )
            # logger.info(response.choices[0]['message']['content'])
            return {"total_tokens": response["usage"]["total_tokens"],
                    "completion_tokens": response["usage"]["completion_tokens"],
                    "content": response.choices[0]['message']['content']}
        except openai.error.RateLimitError as error:
            # rate limit exception
            logger.warning(error)
            if retry_count < 1:
                time.sleep(5)
                logger.warning(
                    "[OPEN_AI] RateLimit exceed, 第%s次重试", retry_count + 1)
                return self.reply_text(query, session_id, retry_count + 1)
            else:
                return {"completion_tokens": 0, "content": "提问太快啦，请休息一下再问我吧"}
        except openai.error.APIConnectionError as error:
            # api connection exception
            logger.warning(error)
            logger.warning("[OPEN_AI] APIConnection failed")
            return {"completion_tokens": 0, "content": "我连接不到你的网络"}
        except openai.error.Timeout as error:
            logger.warning(error)
            logger.warning("[OPEN_AI] Timeout")
            return {"completion_tokens": 0, "content": "我没有收到你的消息"}
        except Exception as ex:
            # unknown exception
            logger.exception(ex)
            Session.clear_session(session_id)
            return {"completion_tokens": 0, "content": "请再问我一次吧"}

    def create_img(self, query, retry_count=0):
        """
        Openai生成用户要求的图片

        Args:
            query (String): 图片要求描述
            retry_count (Numbers, optional): 重试次数. Defaults to 0.

        Returns:
            img: 图片url链接
        """
        try:
            logger.info("[OPEN_AI] image_query=%s", query)
            response = openai.Image.create(
                prompt=query,  # 图片描述
                n=1,  # 每次生成图片的数量
                size="256x256"  # 图片大小,可选有 256x256, 512x512, 1024x1024
            )
            image_url = response['data'][0]['url']
            logger.info("[OPEN_AI] image_url=%s", image_url)
            return image_url
        except openai.error.RateLimitError as error:
            logger.warning(error)
            if retry_count < 1:
                time.sleep(5)
                logger.warning(
                    "[OPEN_AI] ImgCreate RateLimit exceed, 第%s次重试", retry_count + 1)
                return self.create_img(query, retry_count + 1)
            else:
                return "提问太快啦，请休息一下再问我吧"
        except Exception as ex:
            logger.exception(ex)
            return None


class Session(object):
    """
    所有用户的会话管理类

    Args:
        object (object): 基本对象

    Returns:
        Session: 所有用户会话管理对象
    """
    @staticmethod
    def build_session_query(query, session_id):
        '''
        build query with conversation history
        e.g.  [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
        :param query: query content
        :param session_id: from session id
        :return: query content with conversaction
        '''
        session = all_sessions.get(session_id, [])
        if len(session) == 0:
            system_prompt = conf().get("character_desc", "")
            system_item = {'role': 'system', 'content': system_prompt}
            session.append(system_item)
            all_sessions[session_id] = session
        user_item = {'role': 'user', 'content': query}
        session.append(user_item)
        return session

    @staticmethod
    def save_session(answer, session_id, total_tokens):
        """
        保存某用户的会话对

        Args:
            answer (String): 返回iu回复
            session_id (String): 用户会话ID
            total_tokens(Numbers): 当前会话返回使用的总tokens数量
        """
        max_tokens = conf().get("conversation_max_tokens")
        if not max_tokens:
            # default 3000
            max_tokens = 1000
        max_tokens = int(max_tokens)

        session = all_sessions.get(session_id)
        if session:
            # append conversation
            gpt_item = {'role': 'assistant', 'content': answer}
            session.append(gpt_item)

        # discard exceed limit conversation
        Session.discard_exceed_conversation(session, max_tokens, total_tokens)

    @staticmethod
    def discard_exceed_conversation(session, max_tokens, total_tokens):
        """
        会话超长处理，如果超过规定的max_tokens数量，会清除先前对话对一些记录

        Args:
            session (List): 用户的会话记录
            max_tokens (Numbers): 最大tokens数量
            total_tokens(Numbers): 当前会话返回使用的总tokens数量
        """
        dec_tokens = int(total_tokens)
        # logger.info("max_tokens={},dec_tokens={}".format(max_tokens, dec_tokens))
        while dec_tokens > max_tokens:
            if len(session) > 3:
                gpt_item = session.pop(1)
                item_tokens = num_tokens_from_message(gpt_item)
                gpt_item = session.pop(1)
                item_tokens += num_tokens_from_message(gpt_item)
                dec_tokens = dec_tokens - item_tokens
            else:
                break

    @staticmethod
    def clear_session(session_id):
        """
        clear the user session.

        Args:
            session_id (String): weichat session_id
        """
        all_sessions[session_id] = []

    @staticmethod
    def clear_all_session():
        """
        clear all users session.
        """
        all_sessions.clear()

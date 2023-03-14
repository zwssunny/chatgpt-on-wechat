
"""
baidu voice service
"""
import time
import wave
from aip import AipSpeech
from common.log import logger
from common.tmp_dir import TmpDir
from voice.voice import Voice
from config import conf

"""
    百度的语音识别API.
    dev_pid:
        - 1936: 普通话远场
        - 1536：普通话(支持简单的英文识别)
        - 1537：普通话(纯中文识别)
        - 1737：英语
        - 1637：粤语
        - 1837：四川话
    要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
    之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
    填入 config.xml 中.
        baiduyuyin:
            appid: '9670645'
            api_key: 'qg4haN8b2bGvFtCbBGqhrmZy'
            secret_key: '585d4eccb50d306c401d7df138bb02e7'
"""


class BaiduVoice(Voice):

    def __init__(self):
        app_id = conf()["baiduyuyin"].get('baidu_app_id')
        api_key = conf()["baiduyuyin"].get('baidu_api_key')
        secert_key = conf()["baiduyuyin"].get('baidu_secret_key')
        self.client = AipSpeech(app_id, api_key, secert_key)
        self.dev_pid = 1936

    def voiceToText(self, voice_file):
        # 识别本地文件
        logger.debug('[Baidu] voice file name={}'.format(voice_file))

        pcm = self.get_pcm_from_wav(voice_file)
        res = self.client.asr(pcm, "pcm", 16000, {"dev_pid": self.dev_pid})
        if res["err_no"] == 0:
            logger.info("百度语音识别到了：{}".format(res["result"]))
            return "".join(res["result"])
        else:
            logger.info("百度语音识别出错了: {}".format(res["err_msg"]))
            if res["err_msg"] == "request pv too much":
                logger.info("  出现这个原因很可能是你的百度语音服务调用量超出限制，或未开通付费")
            return ""

    def textToVoice(self, text):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5, 'pit': 5, 'vol': 5, 'per': 111
        })
        if not isinstance(result, dict):
            fileName = TmpDir().path() + '语音回复_' + str(int(time.time())) + '.mp3'
            with open(fileName, 'wb') as f:
                f.write(result)
            logger.info(
                '[Baidu] textToVoice text={} voice file name={}'.format(text, fileName))
            return fileName
        else:
            logger.error('[Baidu] textToVoice error={}'.format(result))
            return None

    def get_pcm_from_wav(self, wav_path):
        """
        从 wav 文件中读取 pcm

        :param wav_path: wav 文件路径
        :returns: pcm 数据
        """
        wav = wave.open(wav_path, "rb")
        return wav.readframes(wav.getnframes())

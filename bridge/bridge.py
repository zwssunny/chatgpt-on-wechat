from bot import bot_factory
from voice import voice_factory
from config import conf, load_config


class Bridge(object):
    def __init__(self):
        pass

    def fetch_reply_content(self, query, context):
        bot_type = conf().get('bot_type')
        return bot_factory.create_bot(bot_type).reply(query, context)

    def fetch_voice_to_text(self, voiceFile):
        asr_engine = conf().get('asr_engine')
        return voice_factory.create_voice(asr_engine).voiceToText(voiceFile)

    def fetch_text_to_voice(self, text):
        tts_engine = conf().get('tts_engine')
        return voice_factory.create_voice(tts_engine).textToVoice(text)

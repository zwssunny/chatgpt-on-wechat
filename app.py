# encoding:utf-8

from config import conf, load_config
from channel import channel_factory
from common.log import logger


if __name__ == '__main__':
    try:
        # load config
        load_config()

        # create channel
        channel_type = conf().get("channel_type")
        channel = channel_factory.create_channel(channel_type)

        # startup channel
        channel.startup()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)

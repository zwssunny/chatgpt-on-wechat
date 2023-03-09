# encoding:utf-8

import tiktoken

MYENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")


def num_tokens_from_message(message):
    """
        Returns the number of tokens used by one message.
        See <https://github.com/openai/openai-python/blob/main/chatml.md>
        for information on how messages are converted to tokens.
    Args:
        message (Dictionary): the Items of messages

    Returns:
        Numbers: tokens numbers
    """
    num_tokens = 4  # every message follows <im_start>{role/name}\\n{content}<im_end>\\n
    for key, value in message.items():
        num_tokens += len(MYENCODING.encode(value))
        if key == "name":  # if there's a name, the role is omitted
            num_tokens += -1  # role is always required and always 1 token
    return num_tokens


def num_tokens_from_messages(messages):
    """
        Returns the number of tokens used by a list of messages.
    Args:
        messages (List): 会话列表[{},{},{}]

    Returns:
        Numbers: tokens numbers
    """
    num_tokens = 0
    for message in messages:
        num_tokens += num_tokens_from_message(message)

    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

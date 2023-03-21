# encoding:utf-8

import tiktoken


class MessagesTokens(object):
    """ 
        Split a string into tokens with OpenAI's tokenize. 
        Returns the number of tokens used by the message.
    """
    #encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")

    def __init__(self, model_name: str):
        self.encoding = tiktoken.encoding_for_model(model_name)

    def num_tokens_from_string(self, string: str) -> int:
        """Returns the number of tokens in a text string."""
        num_tokens = len(self.encoding.encode(string))
        return num_tokens

    def num_tokens_from_message(self, message) -> int:
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
            num_tokens += self.num_tokens_from_string(value)
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
        return num_tokens

    def num_tokens_from_messages(self, messages) -> int:
        """
            Returns the number of tokens used by a list of messages.
        Args:
            messages (List): 会话列表[{},{},{}]

        Returns:
            Numbers: tokens numbers
        """
        num_tokens = 0
        for message in messages:
            num_tokens += self.num_tokens_from_message(message)

        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

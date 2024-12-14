from langchain_openai import ChatOpenAI

class GPTHandler:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(openai_api_key=api_key)

    def invoke(self, messages, max_tokens=4096):
        return self.llm.invoke(messages, max_tokens=max_tokens)
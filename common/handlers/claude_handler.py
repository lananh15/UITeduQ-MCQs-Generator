from langchain_anthropic import ChatAnthropic

class ClaudeHandler:
    def __init__(self, api_key):
        self.llm = ChatAnthropic(anthropic_api_key=api_key, model="claude-3-sonnet-20240229")

    def invoke(self, messages, max_tokens=4096):
        return self.llm.invoke(messages, max_tokens=max_tokens)
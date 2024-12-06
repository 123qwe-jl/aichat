import streamlit as st
# from streamlit_chat import message
from openai import OpenAI


API_BASE = "your model url"  #for example:https://open.bigmodel.cn/api/paas/v4/
API_KEY = "your api key"  #api key

client = OpenAI(
  api_key=API_KEY,
  base_url=API_BASE
)
if 'history' not in st.session_state:
    st.session_state['history'] = [{"role": "system", "content": "Hello, I am an AI assistant. How can I help you?"}]

class StreamAIReply:
    def __init__(self, user_input, history):
        self.user_input = user_input
        self.history = history
        self.text = []

    def __iter__(self):
        self.history.append({"role": "user", "content": self.user_input})

        # 使用流式 API 进行对话
        completion = client.chat.completions.create(
            model="glm-4-flash",#根据实际替换
            messages=self.history,
            stream=True,
        )

        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content
                self.text.append(content)

    def get_full_reply(self):
        # 当流式输出完成后，返回完整的文本
        return ''.join([str(item) for item in self.text if item is not None])
def get_ai_reply(user_input):
    reply = StreamAIReply(user_input, st.session_state['history'])
    return reply
if __name__ == "__main__":
# 测试持续对话
    # i = 1
    # while True:
    #     #print(f'第{i}次对话')
    #     user_input = input("\n我:")
    #     print('aichat:',end='')
    #     if len(user_input)==0:
    #         break

    #     assistant_reply = get_ai_reply(user_input)
    #     history.append({"role": "assistant", "content": assistant_reply})
    #     # print(history)

    #     i+=1
    
    st.title('我是chatAI小助手，欢迎使用！')
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    for i in range(0, len(st.session_state['generated']), 1):  # 显示
        with st.chat_message("user"):
            st.write(st.session_state['past'][i])  # 用户输入
        with st.chat_message('assistant'):
            st.write(st.session_state['generated'][i])
    
    # user_input = st.text_input("请输入您的问题：", key="input")
    prompt = st.chat_input("Say something")
    if prompt:
        st.write(f"我：{prompt}")  
        output=get_ai_reply(prompt)
        with st.chat_message("assistant"):
            st.write_stream(output)
        st.session_state['past'].append(prompt)
        st.session_state['generated'].append(output.get_full_reply())
        st.session_state['history'].append({"role": "assistant", "content": output.get_full_reply()})
        
        







    
    
# pip install streamlit streamlit-chat

# prompt = st.chat_input("Enter your prompt here:")
# if prompt:
#     st.write(f"You entered: {prompt}")
#     st.response(f"Response to your prompt: {prompt}")

import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
import utils as util

from my_logging import setup_logger
logger = setup_logger("MyLogger")


def on_input_change():
    user_input = st.session_state.user_input
    logger.info(f"User input changed: {user_input}")
    print(f"User input changed: {user_input}")
    # print(f"st.session_state.past: {st.session_state.past}")
    # print(f"st.session_state.generated: {st.session_state.generated}")
    # print("-----------------------------")
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")
    # print(f"**********st.session_state.past: {st.session_state.past}")
    # print(
    #     f"**********st.session_state.generated: {st.session_state.generated}")


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]
    print(f"len st.session_state.past : {len(st.session_state.past)}")
    print(
        f"len st.session_state.generated : {len(st.session_state.generated)}")


st.session_state.setdefault(
    'past',
    []
)
st.session_state.setdefault(
    'generated',
    [{}]
)

st.title("Chat placeholder")

chat_placeholder = st.empty()

with chat_placeholder.container():
    cnt = len(st.session_state['generated'])
    i = cnt - 1
    for i in range(cnt):
        if i + 1 == cnt:
            print(f"i in iffffff : {i}")
            continue

        print(f"\n\n\niiiiii : {i} cccccccccnt : {cnt}")

        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        user_input = st.session_state['past'][i]
        # print(
        #     f"iiiiiiii : {i}  user_input : {user_input}")
        resp = util.get_ai_answer_for_simple_ui(user_input)
        # print(f"rrrrrrrrrresp : {resp}")
        st.session_state['generated'][i] = resp

        st.session_state.user_input = ""
        logger.info(f"Output from Open AI : {resp}")
        message(
            resp,
            key=f"{i}",
            allow_html=True,
            is_table=False
        )

st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change,
                  key="user_input", value="")
    # st.text_input("User Input:", key="user_input", value="")

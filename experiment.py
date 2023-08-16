import requests
import streamlit as st
from streamlit_lottie import st_lottie

import torch
from transformers import pipeline

from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline

# Helper functions
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def change_session_state():
    st.session_state["run started"] = True

# ASSETS
lottie_robot = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_eZGSBU1hRJ.json")

# PAGE INFO
st.set_page_config(page_title="EHR Capture", page_icon=":mechanical_arm:") #, layout="wide")

# CSS
local_css("style/style.css")

# Load Models
dolly = 'C:/Users/c062387/OneDrive - Thrivent Financial/Documents/Documents/UW Analytics Team/GitRepos/question-answer-app/dolly/'
xdoc = 'C:/Users/c062387/OneDrive - Thrivent Financial/Documents/Documents/UW Analytics Team/GitRepos/question-answer-app/xdoc/squad2/'

@st.cache_data
def get_models(dolly, xdoc):
    generate_text = pipeline(model=dolly, torch_dtype=torch.bfloat16,
                            trust_remote_code=True, device_map="auto", return_full_text=True)

    # qa_model = pipeline('question-answering', model=xdoc, tokenizer=xdoc)

    return generate_text #, qa_model

# generate_text, qa_model = get_models(dolly, xdoc)
generate_text = get_models(dolly, xdoc)

# Dolly Template
prompt_with_context = PromptTemplate(
    input_variables=["instruction", "context"],
    template="{instruction}\n\nInput:\n{context}")

hf_pipeline = HuggingFacePipeline(pipeline=generate_text)

llm_context_chain = LLMChain(llm=hf_pipeline, prompt=prompt_with_context)

# Ask questions
def ask_xdoc(question, context):
    return qa_model({'question': question,'context': context}).get('answer')

def ask_dolly(question, context):
    return llm_context_chain.predict(instruction=question, context=context).lstrip()


# HEADER SECTION
with st.container():
    st_lottie(lottie_robot, height=200, key="robot")
    row1_col1, row1_col2, row1_col3 = st.columns((1, 3, 1))
    with row1_col1:
        pass
    with row1_col2:
        st.markdown("<h1 style='text-align: center;'>LLM Experimentation</h1>", unsafe_allow_html=True)
    with row1_col3:
        pass

    st.write("##")

    with st.form('my_form'):

        context = st.text_area('Enter the context', 'George Washington (February 22, 1732[b] - December 14, 1799) was an American military officer, statesman, and Founding Father who served as the first president of the United States from 1789 to 1797.')

        question = st.text_area('Enter your question', value='When was George Washington president?')

        submitted = st.form_submit_button('Ask')

        if submitted:
            col1, col2 = st.columns((1, 1))

            with col1:
                st.markdown('**XDoc Response**')
                # st.info(ask_xdoc(question, context))

            with col2:
                st.markdown('**Dolly Response**')
                st.info(ask_dolly(question, context))
        
        else:            
            col1, col2 = st.columns((1, 1))

            with col1:
                st.markdown('**XDoc Response**')

            with col2:
                st.markdown('**Dolly Response**')



# question = "When was George Washington president?"
# context = """George Washington (February 22, 1732[b] - December 14, 1799) was an American military officer, statesman,
# and Founding Father who served as the first president of the United States from 1789 to 1797."""




# print(llm_context_chain.predict(instruction=question, context=context).lstrip())

# qa_model({'question': question,'context': context}).get('answer')


import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pdfplumber
from transformers import pipeline

model_response = ""
doc = ""

# FUNCTIONS
def question_answer(question, context, model_name = "microsoft/xdoc-base-squad2.0"):
    model = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    return model(QA_input).get('answer')

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
st.set_page_config(page_title="EHR Capture", page_icon=":mechanical_arm:", layout="wide")

# CSS
local_css("style/style.css")

# HEADER SECTION
with st.container():
    st_lottie(lottie_robot, height=200, key="robot")
    row1_col1, row1_col2, row1_col3 = st.columns((1, 3, 1))
    with row1_col1:
        pass
    with row1_col2:
        st.markdown("<h1 style='text-align: center;'>EHR Capture</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Empowering Insights from Text</h3>", unsafe_allow_html=True)
    with row1_col3:
        pass

    st.write("##")

with st.container():
    row2_col1, row2_col2, row2_col3 = st.columns((1, 1, 1))
    row3_col1, row3_col2, row3_col3 = st.columns((1, 1, 1))
    row4_col1, row4_col2, row4_col3 = st.columns((1, 1, 1))

    with row2_col2:
        uploaded_file = row2_col2.file_uploader("", on_change=change_session_state, type="pdf")
        if uploaded_file is not None:
            pdf = pdfplumber.open(uploaded_file)
            pages = pdf.pages
            doc = ""
            for p in pdf.pages:
                doc += p.extract_text()

    with row3_col2:
        st.subheader("")
        st.subheader("Human Input")
        question = st.text_input(label="", value="Enter your question")

        if question != 'Enter your question':
            model_response = question_answer(question=question, context=doc, model_name = "microsoft/xdoc-base-squad2.0")

    with row4_col2:
        st.divider()
        st.subheader("AI Output")
        st.write(model_response)
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from pdf_functions import *
from transformer_functions import *
import pdfplumber

# FUNCTIONS
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

# CONSTANTS
png_dir = "C:/Users/C082494/PycharmProjects/EHR_v1_000/99 Supporting Files - Dont Touch/02 PDF pngs/"

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
    row4_col1, row4_col2, row4_col3 = st.columns((5, 1, 5))
    row5_col1, row5_col2, row5_col3 = st.columns((1, 1, 1))

    with row2_col2:
        uploaded_file = row2_col2.file_uploader("", on_change=change_session_state, type="pdf")
        doc = ""
        if uploaded_file is not None:
            pdf = pdfplumber.open(uploaded_file)
            pages = pdf.pages
            doc = ""
            for p in pdf.pages:
                doc += p.extract_text()

    st.write("##")
    with row3_col2:
        st.subheader("")
        st.subheader("Human Input")
        question = st.text_input(label="", value="Enter your question")

    with row4_col2:
        operate_button = st.button('Ask')
        model_response = ""
        if operate_button:
            model_response = question_answer(question=question, context=doc, model_name = "microsoft/xdoc-base-squad2.0")

    with row5_col2:
        # modelresponse = model_function(input)
        # st.text_area(label="", value=doc, height=100)
        st.divider()
        st.subheader("AI Output")
        st.write(model_response)
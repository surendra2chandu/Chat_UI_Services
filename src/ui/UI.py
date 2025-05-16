# Import necessary libraries
import sys
# For local testing
# sys.path.append(r'D:\git\ARES_Chat_UI_Services')

# For container testing
sys.path.append(r'/code')

from src.api.StoreDoc import FileUploader
import streamlit as st
from src.conf.Configurations import categories

# Initialize session state variables and rerun the app if needed
if "reset_app" in st.session_state and st.session_state.reset_app:
    st.session_state.uploader_key = st.session_state.get("uploader_key", 0) + 1
    st.session_state.reset_app = False
    st.rerun()

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


# Create a container with a title and border
container = st.container(height=120, border=True)
container.title("ARES File Upload Service")

# File uploader for uploading files
upload_file = st.file_uploader(
    label="Upload a file",
    type=["docx", "txt", "md", "html", " pptx", "pdf"],
    key=f"file_uploader_{st.session_state.uploader_key}")

# Dropdown menu for category selection
category = st.selectbox(
    label="Select a category",
    options=categories.keys())

# Columns for buttons
col1, col2 = st.columns([1, 1])
with col1:
    submit = st.button("Submit", key="submit_button")

with col2:
    if st.button("Refresh", key="refresh_button"):
        st.session_state.reset_app = True
        st.rerun()

# Set custom CSS for the button
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #3E3A47;
            color: white;
            padding: 10px 32px;
            font-size: 16px;
            margin: 3px 2px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True)

st.session_state.page = False

# Handle the submit button click
if submit:
    if upload_file is not None:
        response = FileUploader(category).upload_single_file(upload_file)

        st.success(response[0])

    else:
        st.error("Please upload a file.")

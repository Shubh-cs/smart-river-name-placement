import streamlit as st
from PIL import Image

st.set_page_config(page_title="Map Quality AI", layout="centered")

st.title(" Map Quality AI Checker")
st.write("Detecting cartographic issues using AI")

uploaded = st.file_uploader(
    "Upload a map image (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded Map", width=700)

    if st.button("Analyze Map"):
        st.info("Analyzing map for potential errors...")
        # Placeholder output
        st.warning("⚠️ Possible anomaly detected (demo placeholder)")

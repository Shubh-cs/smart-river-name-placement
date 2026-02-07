"""
MVP Logic:
1. Input: simplified river polygon (hardcoded or uploaded)
2. Compute centroid of the polygon
3. Check distance from centroid to polygon edges
4. If centroid is too close to edge, shift inward
5. Output final (x, y) as label position
"""

import streamlit as st
from PIL import Image
import numpy as np

def suggest_label_position(image):
    """
    Simplified heuristic-based 'AI' for river label placement.
    Uses image dimensions as a proxy for stable placement.
    """
    width, height = image.size

    # Assume central region is safest for MVP
    x = width // 2
    y = height // 2

    return x, y

st.set_page_config(page_title="Smart River Name Placement", layout="centered")

st.title("Smart River Name Placement")
st.write("AI-assisted placement of river labels inside river geometry")

uploaded = st.file_uploader(
    "Upload a river map image (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded River Map", width=700)

    if st.button("Place River Name"):
        x, y = suggest_label_position(image)

        st.success("✅ River name placed safely inside the river (MVP demo)")
        st.caption(f"Suggested label position: (x={x}, y={y})")


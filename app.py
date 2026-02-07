"""
MVP Logic:
1. Detect river pixels using color heuristics (blue detection)
2. Estimate river center from detected pixels
3. Place river name at safest central location
4. Show visible marker + label for demo clarity
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def get_font(image_width):
    """
    Scale font size based on image width so text is visible on phone & demo.
    """
    font_size = max(24, image_width // 20)  # adaptive size

    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        return ImageFont.load_default()


def find_river_center(image):
    img = np.array(image)

    # Detect blue-ish pixels (river approximation)
    blue_mask = (
        (img[:, :, 2] > 120) &   # Blue high
        (img[:, :, 0] < 120) &   # Red low
        (img[:, :, 1] < 120)     # Green low
    )

    coords = np.column_stack(np.where(blue_mask))

    if len(coords) == 0:
        h, w, _ = img.shape
        return w // 2, h // 2

    y_mean, x_mean = coords.mean(axis=0)
    return int(x_mean), int(y_mean)


st.set_page_config(page_title="Smart River Name Placement", layout="centered")

st.title("Smart River Name Placement")
st.write("AI-assisted placement of river labels inside river geometry")

uploaded = st.file_uploader(
    "Upload a river map image (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Uploaded River Map", width=700)

    river_name = st.text_input("Enter river name", value="here..")

    if st.button("Place River Name"):
        draw = ImageDraw.Draw(image)

        # Get suggested position
        x, y = find_river_center(image)
        #FONT SCALING BASED ON IMAGE SIZE 
        img_width, img_height = image.size
        font_size = max(28, img_width // 18)  # dynamic & visible on large maps

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = get_font(image.size[0])



        # DEBUG MARKER (guaranteed visible)
        draw.ellipse(
            [(x - 10, y - 10), (x + 10, y + 10)],
            fill="red"
        )

        #CENTER TEXT PROPERLY
        bbox = draw.textbbox((0, 0), river_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = x - text_width // 2
        text_y = y - text_height // 2


        # Thick white outline
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                draw.text((text_x + dx, text_y + dy), river_name, fill="white", font=font)

        # Main text (dark blue)
        draw.text((text_x, text_y), river_name, fill="#0033cc", font=font)


        st.image(image, caption="River Name Placed (MVP Demo)", width=700)

        st.success("✅ River name placed using heuristic-based river detection")
        st.caption(f"Suggested label position: (x={x}, y={y})")

        st.info(
            "Note: This MVP uses color-based heuristics to approximate river geometry. "
            "Exact GIS vector extraction is out of scope for this demo."
        )

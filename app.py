import streamlit as st
import mediapipe as mp
import numpy as np
import cv2
from PIL import Image
import io

def remove_background(image):
    # Initialize MediaPipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
    
    # Convert PIL Image to OpenCV format
    image_cv = np.array(image)
    
    # Convert RGB to BGR for OpenCV
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
    
    # Process the image
    results = selfie_segmentation.process(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    
    # Get condition and mask
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    
    # Create transparent background
    bg_image = np.zeros(image_cv.shape, dtype=np.uint8)
    bg_image[:] = (0, 0, 0, 0)
    
    # Convert background to RGBA
    bg_image = cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGBA)
    
    # Convert foreground to RGBA
    fg_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGBA)
    
    # Combine foreground and background
    output_image = np.where(condition, fg_image, bg_image)
    
    # Convert back to PIL Image
    return Image.fromarray(output_image)

# Page config
st.set_page_config(page_title="Background Remover", page_icon="🖼️", layout="centered")

# Main UI
st.title("🖼️ Background Remover")
st.markdown("""
Upload an image to remove its background automatically.
- Free to use
- No API key needed
- Local processing
- Supports PNG and JPEG formats
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display original and processed images side by side
    col1, col2 = st.columns(2)
    
    # Original image
    with col1:
        st.markdown("### Original Image")
        image = Image.open(uploaded_file)
        st.image(image)
        
        if st.button("Remove Background"):
            with st.spinner("Processing... This may take a moment."):
                try:
                    # Process the image
                    output_image = remove_background(image)
                    
                    # Display result
                    with col2:
                        st.markdown("### Result")
                        st.image(output_image)
                        
                        # Convert to bytes for download
                        buf = io.BytesIO()
                        output_image.save(buf, format='PNG')
                        byte_im = buf.getvalue()
                        
                        # Download button
                        st.download_button(
                            label="Download Result",
                            data=byte_im,
                            file_name="removed_background.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Tips
with st.expander("Tips for best results"):
    st.markdown("""
    - Use images with clear subjects
    - Ensure good lighting
    - Keep the subject in focus
    - Avoid complex backgrounds
    - Best results with people and objects in the foreground
    """)

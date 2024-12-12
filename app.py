import streamlit as st
import requests
from PIL import Image
import io

# API Configuration
API_KEY = 'LoM2Yq9R78eNzYGsz9ySbqXa'

def remove_background(image_file):
    """Remove background using remove.bg API"""
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_file},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY},
    )
    if response.status_code == requests.codes.ok:
        return response.content
    else:
        return None

# Page config
st.set_page_config(
    page_title="Background Remover",
    page_icon="🖼️",
    layout="centered"
)

# Main UI
st.title("🖼️ Background Remover")
st.markdown("""
Upload an image to remove its background automatically.
- Supports PNG and JPEG formats
- Provides transparent background
- Quick processing
""")

# File uploader
upload = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if upload:
    col1, col2 = st.columns(2)
    
    # Display original image
    with col1:
        st.markdown("### Original Image")
        st.image(upload)
        
        if st.button("Remove Background"):
            with st.spinner("Processing..."):
                try:
                    # Process image
                    output = remove_background(upload)
                    
                    if output:
                        with col2:
                            st.markdown("### Result")
                            st.image(output)
                            
                            # Download button
                            st.download_button(
                                "Download Result",
                                output,
                                file_name="no_background.png",
                                mime="image/png"
                            )
                    else:
                        st.error("Error processing image. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Tips section
st.markdown("---")
with st.expander("Tips for best results"):
    st.markdown("""
    - Use clear, well-lit images
    - Ensure subject is clearly visible
    - Avoid complex patterns
    - Image should be less than 25 MB
    - Higher quality images work better
    """)

# Progress tracker
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = 0

if st.session_state.processed_images > 0:
    st.markdown(f"Images processed this session: {st.session_state.processed_images}")

# Add a warning about processing time
st.info("Note: Processing may take a few seconds depending on image size.")

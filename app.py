import streamlit as st
import requests
from PIL import Image
import io

def remove_background(image_file, api_key):
    """Remove background using remove.bg API"""
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_file},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key},
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

# API Key input
api_key = st.text_input("Enter your remove.bg API key", type="password")
st.markdown("Get your API key at [remove.bg](https://www.remove.bg/api)")

# File uploader
upload = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if upload and api_key:
    col1, col2 = st.columns(2)
    
    # Display original image
    with col1:
        st.markdown("### Original Image")
        st.image(upload)
        
        if st.button("Remove Background"):
            with st.spinner("Processing..."):
                try:
                    # Process image
                    output = remove_background(upload, api_key)
                    
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
                        st.error("Error processing image. Please check your API key.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

elif upload:
    st.warning("Please enter your API key to process images.")

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

# Footer
st.markdown("---")
st.markdown("""
💡 **Note**: You'll need a remove.bg API key to use this tool. 
Get one for free at [remove.bg](https://www.remove.bg/api)
""")

# Add a warning about processing time
st.info("Note: Processing may take a few seconds depending on image size.")

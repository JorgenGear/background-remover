import streamlit as st
from rembg import remove
from PIL import Image
import io
import time

def process_image(upload):
    """Remove background from uploaded image"""
    # Convert uploaded file to bytes
    if upload is not None:
        image = Image.open(upload)
        # Create a bytes object for the output
        output_bytes = io.BytesIO()
        # Remove background
        output = remove(image)
        # Save to bytes object
        output.save(output_bytes, format='PNG')
        return output_bytes.getvalue()
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
- Transparent background in output
- Free to use
""")

# File uploader
upload = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

col1, col2 = st.columns(2)

# Display original image
if upload is not None:
    with col1:
        st.markdown("### Original Image")
        st.image(upload)
        
        # Add processing button
        if st.button("Remove Background"):
            with st.spinner("Processing image..."):
                # Process the image
                output = process_image(upload)
                
                # Display result
                if output is not None:
                    with col2:
                        st.markdown("### Result")
                        st.image(output)
                        
                        # Download button
                        st.download_button(
                            "Download Result",
                            output,
                            file_name="background_removed.png",
                            mime="image/png"
                        )

# Footer with tips
st.markdown("---")
with st.expander("Tips for best results"):
    st.markdown("""
    - Use images with clear subjects
    - Ensure good lighting
    - Avoid complex backgrounds
    - Higher resolution images work better
    - Make sure subject is in focus
    """)

# Add a warning about processing time
st.info("Note: Processing may take a few seconds depending on image size.")

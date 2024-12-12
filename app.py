import streamlit as st
from PIL import Image
from background_removal import BackgroundRemoval

def remove_background(image):
    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Remove background
    output = BackgroundRemoval().remove_background(img_byte_arr)
    return output

# Page config
st.set_page_config(page_title="Background Remover", page_icon="🖼️", layout="centered")

# Main UI
st.title("🖼️ Background Remover")
st.markdown("""
Upload an image to remove its background automatically.
- Free to use
- No API key needed
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
                    output = remove_background(image)
                    
                    # Display result
                    with col2:
                        st.markdown("### Result")
                        st.image(output)
                        
                        # Download button
                        st.download_button(
                            label="Download Result",
                            data=output,
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
    """)

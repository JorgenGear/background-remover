import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

def remove_background(image, threshold=240):
    # Convert the image to RGBA if it isn't already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Convert to numpy array
    data = np.array(image)
    
    # Calculate the average of RGB channels
    rgb_avg = np.mean(data[:, :, :3], axis=2)
    
    # Create an alpha mask based on the brightness
    alpha_mask = (rgb_avg < threshold).astype(np.uint8) * 255
    
    # Apply the mask to the alpha channel
    data[:, :, 3] = alpha_mask
    
    # Convert back to PIL Image
    return Image.fromarray(data)

# Page config
st.set_page_config(page_title="Background Remover", page_icon="🖼️", layout="centered")

# Main UI
st.title("🖼️ Background Remover")
st.markdown("""
Upload an image to remove light backgrounds automatically.
- Free to use
- No API needed
- Works best with light backgrounds
- Supports PNG and JPEG formats
""")

# Add threshold slider
threshold = st.slider("Brightness Threshold (adjust if needed)", 
                     min_value=0, 
                     max_value=255, 
                     value=240,
                     help="Lower value = keep more pixels, Higher value = remove more pixels")

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
            with st.spinner("Processing..."):
                try:
                    # Process the image
                    output_image = remove_background(image, threshold)
                    
                    # Display result
                    with col2:
                        st.markdown("### Result")
                        st.image(output_image)
                        
                        # Convert to bytes for download
                        buf = BytesIO()
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
    - Use images with light backgrounds
    - Ensure good contrast between subject and background
    - Adjust the threshold slider if needed:
        - Lower values keep more of the image
        - Higher values remove more pixels
    - Best results with product photos on white backgrounds
    """)

# Add note about limitations
st.markdown("---")
st.markdown("""
💡 **Note**: This simple version works best with light backgrounds. 
For better results with complex backgrounds, you might want to try professional tools.
""")

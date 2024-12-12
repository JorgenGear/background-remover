import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

def remove_background(image):
    # Convert PIL Image to OpenCV format
    opencv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Create a mask initialized with obvious background (2) and probable background (0)
    mask = np.zeros(opencv_img.shape[:2], np.uint8)
    
    # Create temporary arrays used by grabCut
    bgd_model = np.zeros((1,65), np.float64)
    fgd_model = np.zeros((1,65), np.float64)
    
    # Define the rectangle that contains the foreground
    rect = (20, 20, opencv_img.shape[1]-20, opencv_img.shape[0]-20)
    
    # Apply grabCut
    cv2.grabCut(opencv_img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Create mask where 0 and 2 are background, 1 and 3 are foreground
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # Multiply image with the mask to get cut-out image
    result = opencv_img * mask2[:, :, np.newaxis]
    
    # Convert to RGBA
    rgba = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    
    # Make all black pixels transparent
    rgba[np.all(result == 0, axis=2)] = [0,0,0,0]
    
    # Convert back to PIL Image
    result_pil = Image.fromarray(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA))
    
    return result_pil

# Page config
st.set_page_config(page_title="Background Remover", page_icon="🎨", layout="wide")

# Main UI
st.title("🎨 Background Remover")
st.markdown("""
Upload an image to remove its background.
- Simple to use
- No API required
- Works best with clear subjects
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Original Image")
        image = Image.open(uploaded_file)
        st.image(image)
        
        if st.button("Remove Background"):
            with st.spinner("Processing... Please wait."):
                try:
                    # Process image
                    result = remove_background(image)
                    
                    # Display result
                    with col2:
                        st.markdown("### Result")
                        st.image(result)
                        
                        # Save for download
                        buf = io.BytesIO()
                        result.save(buf, format='PNG')
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
    - Ensure good contrast between subject and background
    - Works best when subject is centered
    - Simple backgrounds give better results
    - Larger images may take longer to process
    """)

# Footer
st.markdown("---")
st.markdown("""
💡 **Note**: This tool uses OpenCV's GrabCut algorithm. Results may vary depending on image complexity.
For professional results, consider using specialized tools.
""")

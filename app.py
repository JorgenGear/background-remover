import streamlit as st
from PIL import Image
import io
import pixellib
from pixellib.tune_bg import alter_bg

def load_model():
    change_bg = alter_bg()
    change_bg.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    return change_bg

# Page configuration
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="🎨",
    layout="wide"
)

# Main UI
st.title("🎨 AI Background Remover")
st.markdown("""
Remove backgrounds from your images using AI!
- Easy to use
- Works with most images
- Free processing
""")

# Create file uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Original Image")
        image = Image.open(uploaded_file)
        st.image(image)
        
        # Save uploaded file temporarily
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Remove Background"):
            try:
                with st.spinner("Processing image..."):
                    # Load model and process image
                    change_bg = load_model()
                    output_path = "output_image.png"
                    change_bg.color_bg("temp_image.png", output_path, 
                                     colors=(0,0,0,0), is_raw=True)
                    
                    # Display result
                    with col2:
                        st.markdown("### Result")
                        output_image = Image.open(output_path)
                        st.image(output_image)
                        
                        # Add download button
                        with open(output_path, "rb") as file:
                            btn = st.download_button(
                                label="Download image",
                                data=file,
                                file_name="removed_background.png",
                                mime="image/png"
                            )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Tips
with st.expander("Tips for best results"):
    st.markdown("""
    - Use clear, well-lit images
    - Ensure subject is in focus
    - Works best with:
        - People
        - Animals
        - Common objects
    - Higher quality images give better results
    """)

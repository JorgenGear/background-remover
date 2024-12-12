import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
import io

def load_model():
    model = hub.load('https://tfhub.dev/tensorflow/lite-model/deeplabv3/1/metadata/2')
    return model

def process_image(image):
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to model input size while maintaining aspect ratio
    target_size = (513, 513)
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array and normalize
    input_tensor = np.array(image)
    input_tensor = tf.cast(input_tensor, tf.float32) / 127.5 - 1
    input_tensor = tf.expand_dims(input_tensor, 0)
    
    return input_tensor, image

def remove_background(model, image):
    # Process image
    input_tensor, resized_image = process_image(image)
    
    # Run model prediction
    predictions = model.signatures['serving_default'](tf.constant(input_tensor))
    mask = tf.argmax(predictions['output'], axis=-1)
    mask = tf.squeeze(mask).numpy()
    
    # Create alpha channel (255 for foreground, 0 for background)
    alpha = np.where(mask > 0, 255, 0).astype(np.uint8)
    
    # Resize alpha back to original image size
    alpha = Image.fromarray(alpha).resize(image.size, Image.Resampling.LANCZOS)
    
    # Add alpha channel to original image
    result = image.copy()
    result.putalpha(alpha)
    
    return result

# Page configuration
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="🎨",
    layout="wide"
)

# Main UI
st.title("🎨 AI Background Remover")
st.markdown("""
Use advanced AI to remove backgrounds from your images!
- Powered by Google's DeepLab V3
- Handles complex backgrounds
- Free to use
""")

# Load model
try:
    with st.spinner("Loading AI model... (this may take a moment on first run)"):
        model = load_model()
        
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image to remove its background"
    )

    if uploaded_file:
        # Create two columns for before/after
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Image")
            # Load and display original image
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            if st.button("Remove Background", use_container_width=True):
                with st.spinner("Processing... Please wait..."):
                    try:
                        # Process image and remove background
                        result = remove_background(model, image)
                        
                        # Display result
                        with col2:
                            st.markdown("### Result")
                            st.image(result, use_column_width=True)
                            
                            # Save for download
                            buf = io.BytesIO()
                            result.save(buf, format='PNG')
                            byte_im = buf.getvalue()
                            
                            # Download button
                            st.download_button(
                                label="Download Result",
                                data=byte_im,
                                file_name="background_removed.png",
                                mime="image/png",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error processing image: {str(e)}")
                        
except Exception as e:
    st.error(f"Error loading model: {str(e)}")

# Tips section
with st.expander("📝 Tips for best results"):
    st.markdown("""
    - Use images with clear subjects
    - Good lighting helps improve results
    - The model works best with:
        - People
        - Animals
        - Common objects
        - Vehicles
    - Complex or blurred edges might need touch-up
    """)

# Footer
st.markdown("---")
st.markdown("""
💡 **Note**: This tool uses Google's DeepLab V3 model for semantic segmentation.
Processing time may vary depending on image size and complexity.
""")

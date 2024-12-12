import streamlit as st
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
import gdown
import os
from u2net import U2NET

def load_model():
    model_path = 'u2net.pth'
    if not os.path.exists(model_path):
        # Download U2NET model
        url = 'https://drive.google.com/uc?id=1tCU5MM1LhRgGou5OpmpjBQbSrYIUoYab'
        gdown.download(url, model_path, quiet=False)
    
    model = U2NET(3, 1)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def preprocess_image(image):
    # Convert PIL image to tensor
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict_mask(model, image):
    # Get prediction
    with torch.no_grad():
        output = model(image)
        pred = F.interpolate(output[0], size=image.shape[2:],
                           mode='bilinear', align_corners=False)
        pred = torch.sigmoid(pred)
        pred = pred.squeeze().cpu().numpy()
    return pred

def remove_background(image, model):
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Preprocess
    input_tensor = preprocess_image(image)
    
    # Predict mask
    mask = predict_mask(model, input_tensor)
    
    # Convert mask to PIL Image
    mask = Image.fromarray((mask * 255).astype(np.uint8))
    mask = mask.resize(image.size)
    
    # Add alpha channel
    result = image.copy()
    result.putalpha(mask)
    
    return result

# Page setup
st.set_page_config(page_title="ML Background Remover", layout="wide")

st.title("🤖 ML-Powered Background Remover")
st.markdown("""
This tool uses U2NET, a deep learning model, to remove backgrounds from images.
- Advanced AI-based removal
- Works with complex backgrounds
- Free to use
""")

# Load model
try:
    with st.spinner("Loading ML model... (this may take a minute on first run)"):
        model = load_model()
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        col1, col2 = st.columns(2)
        
        # Display original image
        with col1:
            st.markdown("### Original Image")
            image = Image.open(uploaded_file)
            st.image(image)
            
            if st.button("Remove Background"):
                with st.spinner("Processing... (this may take a few seconds)"):
                    # Process image
                    result = remove_background(image, model)
                    
                    # Display result
                    with col2:
                        st.markdown("### Result")
                        st.image(result)
                        
                        # Save for download
                        output = BytesIO()
                        result.save(output, format='PNG')
                        
                        st.download_button(
                            "Download Result",
                            output.getvalue(),
                            "background_removed.png",
                            "image/png"
                        )
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Tips
with st.expander("Tips for best results"):
    st.markdown("""
    - Works well with most types of images
    - Better results with clear subjects
    - Can handle complex backgrounds
    - Processing larger images takes more time
    - Model works best when subject is clearly visible
    """)

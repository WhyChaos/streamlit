import streamlit as st
from PIL import Image, ImageFilter
import io

def apply_filter(image, filter_type):
    if filter_type == "Blur":
        return image.filter(ImageFilter.BLUR)
    elif filter_type == "Contour":
        return image.filter(ImageFilter.CONTOUR)
    elif filter_type == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    else:
        return image

def main():
    st.title("Image Processing App")
    
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        filter_type = st.selectbox("Select a filter", ["Original", "Blur", "Contour", "Sharpen"])
        filtered_image = apply_filter(image, filter_type)
        st.image(filtered_image, caption=f"{filter_type} Image", use_column_width=True)
        
        # Create a button to download the processed image
        download_button(filtered_image, f"{filter_type.lower()}_image")
    
def download_button(image, filename):
    # Create a streamlit button with a download link for the image
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    st.download_button(
        label="Download Processed Image",
        data=buffered.getvalue(),
        file_name=f"{filename}.png",
        mime="image/png",
    )

if __name__ == "__main__":
    main()

import io

def download_image(col, image, filename):
    # Create a streamlit button with a download link for the image
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    col.download_button(
        label="下载图片",
        data=buffered.getvalue(),
        file_name=f"{filename}.png",
        mime="image/png",
    )
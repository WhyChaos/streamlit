from PIL import Image, ImageDraw

# 打开图片
image = Image.open('/home/hc/streamlit/augraphy_cache/image_0.png')
image = image.rotate(angle=340, expand=False)

image.save('output.jpg')
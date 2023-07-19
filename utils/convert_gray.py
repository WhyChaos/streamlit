from PIL import Image

def convert_gray(image):
     # 获取图像的宽度和高度
    width, height = image.size

    # 创建一个新的空白图像，模式为RGB
    black_and_white_image = Image.new("RGB", (width, height))

    # 遍历图像的每个像素，并将其设置为黑白颜色
    for x in range(width):
        for y in range(height):
            # 获取原图像像素的颜色
            r, g, b = image.getpixel((x, y))
            # 计算灰度值
            gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            # 将新图像的像素设置为灰度值
            black_and_white_image.putpixel((x, y), (gray, gray, gray))

    return black_and_white_image
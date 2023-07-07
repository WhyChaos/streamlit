def dark(img, coordinate):
    x1, y1, x2, y2 = map(int, coordinate)
    for x in range(x1, x2, 1):
        for y in range(y1, y2, 1):
            img.putpixel((x, y), (0, 0, 0))
    return img

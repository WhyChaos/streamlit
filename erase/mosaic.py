def _mosaic(img):
    s = img.size
    img = img.resize((int(s[0]/10)+1, int(s[1]/10)+1))
    img = img.resize(s)
    return img


def mosaic(img, coordinate):
    x1, y1, x2, y2 = map(int, coordinate)
    c = img.crop((x1, y1, x2, y2))
    c = _mosaic(c)
    img.paste(c, (x1, y1, x2, y2))
    return img

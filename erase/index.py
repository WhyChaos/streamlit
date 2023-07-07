# import dark
from erase import mosaic
from erase import dark


def erase(image, coordinate_list, type='mosaic'):
    for coordinate in coordinate_list:
        if type == 'mosaic':
            image = mosaic.mosaic(image, coordinate)
        elif type == 'dark':
            image = dark.dark(image, coordinate)
    return image

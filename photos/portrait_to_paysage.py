from PIL import Image, ImageEnhance, ImageFilter

def detect_orientation(image):
    if image.width < image.height:
        return True
    else:
        return False


def resize_to_portrait_height(image):
    new_size = (int(image.width * (image.width/image.height))\
                        , image.width)

    return image.resize(new_size)


def apply_blur(image, factor=10):
    image = image.filter(ImageFilter.GaussianBlur(factor))

    return image


def apply_gradient(image, max_factor=.9, step=1, direction='right'):
    upper, lower = 0, image.height
    factor = 0

    gradient_range = range(0,image.width + 1, step)

    if direction == 'right':
        gradient_range = gradient_range[::-1]

    for i in gradient_range:
        left, right = i, i + step
        coordinates = (left, upper, right, lower)
        band = image.crop(coordinates)

        factor += step * (float(max_factor)/image.width)

        enhancer = ImageEnhance.Brightness(band)
        band = enhancer.enhance(factor)

        image.paste(band, coordinates)

    return image


def add_side_images(image, width):
    right_side = apply_blur(image)
    right_side = right_side.transpose(Image.FLIP_LEFT_RIGHT)
    left_side = right_side.copy()
    
    right_side = apply_gradient(right_side, direction='right')
    left_side = apply_gradient(left_side, direction='left')

    new_image = Image.new('RGB', (width, image.height))

    side_size = int((width - image.width) / 2)

    left_side = left_side.resize((side_size, image.height))
    new_image.paste(left_side, (0,0))
    new_image.paste(image, (side_size, 0))

    if width - image.width % 2 == 0:
        right_side = right_side.resize((side_size, image.height))
        new_image.paste(right_side, (side_size + image.width, 0))
    else:
        right_side = right_side.resize((side_size - 1, image.height))
        new_image.paste(right_side, (side_size + image.width, 0))

    return new_image


def portrait_to_paysage(image):
    if detect_orientation(image):
        width = image.height
        image = resize_to_portrait_height(image)
        return add_side_images(image, width)

    else:
        return image


if __name__ == '__main__':
    #test
    image = Image.open("/home/vifespoir/github/blog/content/images/Roses-Cadaques_6-12-2015/WP_20150911_16_54_30_Pro.jpg")
    portrait_to_paysage(image)

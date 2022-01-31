import imghdr
from PIL import Image
from io import BytesIO
from django.core.files import File


def aspect_ratio(width, height):
    """
    Module to adjust the aspect ratio of the media file
    """
    new_height = height
    new_width = width

    aspect_ratio = round(float(width/height), 1)

    # changing to 7:10 aspect ratio values
    if aspect_ratio > 0.7:
        new_height = height
        new_width = int(round((height*0.7), 0))

    elif aspect_ratio < 0.7:
        new_height = int(width/0.7)
        new_width = width

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    return left, top, right, bottom


def compress_media(file):
    """
    INTO COMPRESSION
    """
    img_ext = ['jpg', 'png', 'webp', 'jpeg', 'jpe', 'jif',
               'jfif', 'jfi', 'tiff', 'tif', 'psd', 'jp2', 'jpf', 'jpx']

    file_ext = imghdr.what(file)

    try:
        # FOR COMPRESSING AN IMAGE
        if file_ext in img_ext:
            picture = Image.open(file).convert("RGB")

            width, height = picture.size  # original size of the image
            # print(height, width)

            left, top, right, bottom = aspect_ratio(width=width, height=height)

            cropped_image = picture.crop((left, top, right, bottom))
            # print("ASPECT RATIO OF COMPRESSED IMAGE IS:",
            #       cropped_image.size[0]/cropped_image.size[1])

            image_io = BytesIO()
            cropped_image.save(image_io,
                               "webp",
                               optimize=True,
                               quality=70)
            final_image = File(image_io, name=file.name)

            return final_image

    except ValueError:
        return 'Media compression error'


# print(compress_media('videoplayback.mp4'))

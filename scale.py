from PIL import Image
import io

Image.MAX_IMAGE_PIXELS = 10000000000


class ImageScaling:

    def __init__(self, scale_factor):
        self.scale_factor = int(scale_factor)

    def image_scale(self, binary_data):
        original_image = Image.open(io.BytesIO(binary_data))
        if original_image.info.__contains__('dpi'):
            dpi = original_image.info['dpi']
        else:
            dpi = (96, 96)
        width, height = original_image.size
        img_byte_arr = io.BytesIO()
        if width > self.scale_factor and height > self.scale_factor:
            new_size = self.__get_scaling_factor(width, height)
            new_image = original_image.resize(new_size, resample=Image.Resampling.LANCZOS, reducing_gap=3.0)
            new_image.save(img_byte_arr, format='JPEG', dpi=dpi, quality=89)
        else:
            return binary_data
        return img_byte_arr.getvalue()

    def __get_scaling_factor(self, width, height):
        if width > height:
            scale = width / self.scale_factor
            height2 = 1
            if scale != 0:
                height2 = int(height / scale)
            return self.scale_factor, height2
        else:
            scale = height / self.scale_factor
            width2 = int(width / scale)
            return width2, self.scale_factor

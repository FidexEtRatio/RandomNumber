import numpy
from PIL import Image
from system_entropy import get_hardware_seed

def xorshift128plus(seed1, seed2):
    s0, s1 = seed1, seed2
    t = s0
    s0 = s1
    s1 = s1 ^ (s1 >> 23) ^ (t ^ (t >> 17) ^ (s0 ^ (s0 >> 26)))
    return s1 + s0

# extract data from the rgb values of the picture
def extract_data_rgb(img_path):
    img = Image.open(img_path)
    data_arr = numpy.array(img)
    height, width, _ = data_arr.shape

    # create a center region, where the sun is approximately 75% of the picture
    # and is perfectly aligned in the center
    center_height = int(height * 0.75)
    center_width = int(width * 0.75)
    start_height = (height - center_height) // 2
    start_width = (width - center_width) // 2
    center_region = data_arr[start_height:start_height + center_height, start_width:start_width + center_width]

    entropy_val = []
    step = 128
    for y in range(0, center_height, step):
        for x in range(0, center_width, step):
            pixel = center_region[y, x]
            pixel = xorshift128plus(pixel % (2 ** 64), get_hardware_seed() % (2 ** 64))
            entropy_val.extend(pixel)
            step = 128 + (x + y) % 129 # step for extra variation
    
    # convert to 1d array with a fixed size of 1000
    return numpy.array(entropy_val, dtype = numpy.uint8).flatten()[:1000]
    
# extract data from the fourier transform
def extract_data_fft(img_path):
    img = Image.open(img_path)
    data_arr = numpy.array(img)

    fft_result = numpy.fft.fft2(data_arr)
    fft_phase = numpy.angle(fft_result)

    # convert to 1d array with a fixed size of 1000
    return fft_phase.flatten()[:1000]
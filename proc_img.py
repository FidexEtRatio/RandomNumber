from img_data_extract import extract_data_fft, extract_data_rgb
from local_img_source import get_images, cleanup
from nasa_source import get_current_sun_data
import numpy

def xor_arrays(arr1, arr2):
    return [int(x) & 0xFFFFFFFF ^ int(y) & 0xFFFFFFFF for x, y in zip(arr1, arr2)]

def get_data_for_base():
    get_current_sun_data()
    img_array = get_images()
    print("Images loaded into program...")

    rgb_arr = []
    fft_arr = []
    for img in img_array:
        print(f"Extracting RGB & FFT Data from image #{len(rgb_arr) + 1}...")
        rgb_data = extract_data_rgb(img)
        fft_data = extract_data_fft(img)
        rgb_arr.append(rgb_data)
        fft_arr.append(fft_data)
    cleanup()

    print("Executing 1st round of XOR-ing...")
    rgb_arr1 = xor_arrays(rgb_arr[0], rgb_arr[2])
    print("Executing 2nd round of XOR-ing...")
    rgb_arr2 = xor_arrays(rgb_arr[1], rgb_arr[3])
    print("Executing 3rd round of XOR-ing...")
    fft_arr1 = xor_arrays(rgb_arr[0], rgb_arr[3])
    print("Executing 4th round of XOR-ing...")
    fft_arr2 = xor_arrays(rgb_arr[1], rgb_arr[2])

    base_data = numpy.concatenate(rgb_arr1, rgb_arr2, fft_arr1, fft_arr2)

    return base_data
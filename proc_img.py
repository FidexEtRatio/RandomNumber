import hashlib
from img_data_extract import extract_data_fft, extract_data_rgb
from local_img_source import get_images, cleanup

def rotate_right(value, n):
    if value > 0xFFFFFFFF:
        print(f"Warning: Value is too large for 32-bit operation: {value}")
    n = n % 32  # Ensure that the number of bits to rotate is within 0-31 range
    value = value & 0xFFFFFFFF  # Ensure the value is within 32-bit bounds
    return ((value >> n) | (value << (32 - n))) & 0xFFFFFFFF

def xor_arrays(arr1, arr2):
    return [int(x) & 0xFFFFFFFF ^ int(y) & 0xFFFFFFFF for x, y in zip(arr1, arr2)]

def get_value():
    img_array = get_images()
    print("Images loaded into program!")
    
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

    print("Executing 5th round of XOR-ing...")
    fin_rgb = xor_arrays(rgb_arr1, rgb_arr2)
    print("Executing 6th round of XOR-ing...")
    fin_fft = xor_arrays(fft_arr1, fft_arr2)

    print("Executing BIT rotation in RGB Data...")
    data = [rotate_right(val, val%10) for val in fin_rgb]

    print("Executing 7th round of XOR-ing...")
    data = xor_arrays(data, fin_fft)
    
    print("Executing BIT rotation in Data list...")
    data = [rotate_right(val, val%10) for val in fin_rgb]

    print("Converting Data list to a single binary string...")
    big_data = list_to_binary_string(data)

    print("Hashing binary string...")
    final = hash_binary_string(big_data)

    return final

def list_to_binary_string(list):
    bin_str = ''.join(format(num, '08b') for num in list)

    return bin_str

def hash_binary_string(bin_str):
    # convert binary string to bytes
    binary_data = int(bin_str, 2).to_bytes((len(bin_str) + 7) // 8, byteorder='big')
    
    # hash data
    hashed = hashlib.sha3_512(binary_data).hexdigest()
    
    return hashed
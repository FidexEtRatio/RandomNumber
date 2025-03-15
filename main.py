from proc_img import get_base
from radio import get_seed
from generator import generate

def main():
    base = get_base()
    count = 1
    for i in range(20):
        with open('numbers.txt', 'ab') as file:
            rand_num = generate(base, get_seed(), 1, 65530, count)
            count += 1
            file.write(rand_num.to_bytes(2, byteorder="big"))
            
if __name__ == "__main__":
    main()
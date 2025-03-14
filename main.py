from proc_img import get_base
from radio import get_seed
from generator import generate

def main():
    base = get_base()
    count = 1
    for i in range(30):
        with open('numbers.txt', 'a') as file:
            rand_num = generate(base, get_seed(), 1, 500, count)
            count += 1
            file.write(str(rand_num) + ", ")  # Write the number to the file as a string

if __name__ == "__main__":
    main()
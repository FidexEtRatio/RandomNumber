from proc_img import get_base
from radio import get_seed
from generator import generate

def main():
    base = get_base()
    rand_num = generate(base, get_seed(), 1, 1000)
    print(f"\n\n--- Random Number: {rand_num} ---")

    rand_num = generate(base, get_seed(), 1, 1000)
    print(f"\n\n--- Random Number: {rand_num} ---")

    rand_num = generate(base, get_seed(), 1, 1000)
    print(f"\n\n--- Random Number: {rand_num} ---")

if __name__ == "__main__":
    main()
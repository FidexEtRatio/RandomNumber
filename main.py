from proc_img import get_data_for_base
from base_data import BaseData
from seed_data import SeedData
from radio import get_data_for_seed
from generator import generate
from audio_entropy import calculate_entropy  # Ensure this function exists

def main():
    base_data_string = get_data_for_base()
    base = BaseData(base_data_string)
    print (f"Base data size: {base.get_len()}")
    count = 1
    total_numbers = 1048576  # Target amount
    batch_size = 65536  # Generate numbers in batches

    entropy_values = []  # Store entropy values for analysis

    seed_data = get_data_for_seed()
    seed = SeedData(seed_data)

    with open('generated_numbers.bin', 'ab') as file:
        for _ in range(total_numbers // batch_size):  # Each batch = 2000 numbers

            batch_data = bytearray()  # Store batch for entropy calculation
            for _ in range(batch_size):
                rand_num = generate(base.get_base(), seed.get_seed(), 1, 65530, count)
                count += 1

                # 📝 Write to numbers.txt
                file.write(rand_num.to_bytes(2, byteorder="big"))
                batch_data.extend(rand_num.to_bytes(2, byteorder="big"))

                # 📢 Check if seed is exhausted and refresh if needed
                if seed.about_to_finish():
                    print(f"Former seed size: {seed.get_len()}")  
                    print("Data from radio has been exhausted. Fetching new data...")
                    seed.update_data(get_data_for_seed())
                if base.about_to_finish():
                    print("Data from base has been exhausted. Fetching new data...")
                    base.update_data(get_data_for_base())

            # 📊 Calculate entropy of this batch
            entropy = calculate_entropy(batch_data)
            entropy_values.append(entropy)
            print(f"Batch entropy: {entropy:.5f}")


    # Compute entropy statistics
    if entropy_values:
        peak_entropy = max(entropy_values)
        low_entropy = min(entropy_values)
        avg_entropy = sum(entropy_values) / len(entropy_values)

        print("\n **Entropy Report** ")
        print(f"Peak Entropy: {peak_entropy:.5f} bits/byte")
        print(f"Low Entropy: {low_entropy:.5f} bits/byte")
        print(f"Average Entropy: {avg_entropy:.5f} bits/byte")

if __name__ == "__main__":
    main()

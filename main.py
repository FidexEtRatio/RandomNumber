from proc_img import get_base
from radio import get_seed
from generator import generate
from audio_entropy import calculate_entropy  # Ensure this function exists

def main():
    base = get_base()
    count = 1
    total_numbers = 50000  # Target amount
    batch_size = 1000  # Generate numbers in batches

    entropy_values = []  # Store entropy values for analysis

    with open('numbers.txt', 'ab') as file:
        for _ in range(total_numbers // batch_size):  
            seed = get_seed()  # Get a single seed and generate a batch from it
            
            batch_data = bytearray()  # Store generated batch for entropy check
            
            for _ in range(batch_size):
                rand_num = generate(base, seed, 1, 65530, count)
                count += 1
                file.write(rand_num.to_bytes(2, byteorder="big"))
                batch_data.extend(rand_num.to_bytes(2, byteorder="big"))  # Collect bytes

            # Calculate entropy of this batch
            entropy = calculate_entropy(batch_data)
            entropy_values.append(entropy)
            print(f"Batch entropy: {entropy:.5f}")

    # Compute entropy statistics
    if entropy_values:
        peak_entropy = max(entropy_values)
        low_entropy = min(entropy_values)
        avg_entropy = sum(entropy_values) / len(entropy_values)

        print("\n🔹 **Entropy Report** 🔹")
        print(f"✅ Peak Entropy: {peak_entropy:.5f} bits/byte")
        print(f"⚠️ Low Entropy: {low_entropy:.5f} bits/byte")
        print(f"📊 Average Entropy: {avg_entropy:.5f} bits/byte")

if __name__ == "__main__":
    main()

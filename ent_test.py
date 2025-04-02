import subprocess
import sys
import os
import re

def run_ent_tests(file_path):
    """Run ent (entropy) tests on the file and provide clearer output."""
    try:
        result = subprocess.run(["ent", file_path], capture_output=True, text=True)
        output = result.stdout
        print("=== ENT Tests ===")
        
        # Extract key metrics
        entropy = float(re.search(r"Entropy = ([0-9\.]+) bits per byte", output).group(1))
        chi_square_match = re.search(r"Chi square distribution for .* is ([0-9\.]+)", output)
        arithmetic_mean = float(re.search(r"Arithmetic mean value of data bytes is ([0-9\.]+)", output).group(1))
        serial_correlation = float(re.search(r"Serial correlation coefficient is ([0-9\.-]+)", output).group(1))
        
        chi_square = float(chi_square_match.group(1)) if chi_square_match else None
        
        # Interpret results
        print(f"Entropy: {entropy} (ideal: 8.0)")
        if entropy >= 7.98:
            print("✅ Entropy test PASSED (indicates randomness)")
        else:
            print("❌ Entropy test FAILED (not sufficiently random)")
        
        if chi_square is not None:
            print(f"Chi-square: {chi_square} (lower is better for randomness)")
        else:
            print("Chi-square value could not be extracted.")
        
        print(f"Arithmetic mean: {arithmetic_mean} (expected ~127.5)")
        print(f"Serial correlation: {serial_correlation} (should be close to 0)")
    
    except FileNotFoundError:
        print("Error: 'ent' is not installed. Please install it and try again.")
    except Exception as e:
        print(f"Error processing ENT output: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python randomness_tester.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print("Error: File not found.")
        sys.exit(1)
    
    run_ent_tests(file_path)

if __name__ == "__main__":
    main()

import struct
import sys
import os

def convert(input_file, output_file):
    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        while chunk := fin.read(2):  # Read 2 bytes at a time
            num = struct.unpack("<H", chunk)[0]  # Convert to 16-bit integer
            bits = format(num, "016b")  # Convert to 16-bit binary string
            fout.write(bits.encode())  # Save as binary text (0s and 1s)

def run_nist_tests(file_path):
    """Run NIST Statistical Test Suite (STS) on the file."""
    if not os.path.exists("sts"):
        print("Error: NIST STS is not installed. Please download and install it.")
        return
    try:
        os.system(f"sts -i {file_path}")
    except FileNotFoundError:
        print("Error: NIST STS is not installed or not in the PATH.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_dieharder.py <file_path> <output_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output = sys.argv[2]
    
    if not os.path.exists(file_path):
        print("Error: File not found.")
        sys.exit(1)

    convert(file_path, output)

    run_nist_tests(output)


if __name__ == "__main__":
    main()

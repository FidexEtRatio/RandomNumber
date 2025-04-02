import struct
import os
import sys
import subprocess

def run_dieharder_tests(file_path):
    """Run Dieharder tests on the file and ensure output is captured."""
    try:
        result = subprocess.run(["dieharder", "-a", "-g", "202", "-f", file_path], capture_output=True, text=True)
        print("=== Dieharder Tests ===")
        if result.stdout.strip():
            print(result.stdout)
        else:
            print(" No output received. Ensure dieharder is correctly installed and the file has enough data.")
    except FileNotFoundError:
        print("Error: 'dieharder' is not installed. Please install it and try again.")

def convert(input_file, output_file):

    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        while chunk := fin.read(2):  # Read 2 bytes
            num = struct.unpack("<H", chunk)[0]  # Convert to unsigned short (16-bit)
            fout.write(struct.pack("<I", num))  # Convert to unsigned int (32-bit)

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

    run_dieharder_tests(output)


if __name__ == "__main__":
    main()

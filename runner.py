import subprocess

def main():
    script_to_run = "main.py"

    for i in range(1000):
        print(f"Execution {i + 1}/1000...")
        subprocess.run(["python3", script_to_run], check=True)

if __name__ == "__main__":
    main()
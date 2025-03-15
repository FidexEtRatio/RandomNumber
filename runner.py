import subprocess

def main():
    script_to_run = "main.py"

    for i in range(2000):
        print(f"Execution {i + 1}/2000...")
        with open('executions_count.txt', 'a') as file:
            print(str(i) + " execution...\n")
        subprocess.run(["python3", script_to_run], check=True)

if __name__ == "__main__":
    main()
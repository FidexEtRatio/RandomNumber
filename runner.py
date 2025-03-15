import subprocess

def main():
    script_to_run = "main.py"

    for i in range(5883):
        print(f"Execution {i + 1}/5883...")
        with open('executions_count.txt', 'a') as file:
            file.write(str(i + 1) + " execution...\n")
        subprocess.run(["python3", script_to_run], check=True)

if __name__ == "__main__":
    main()
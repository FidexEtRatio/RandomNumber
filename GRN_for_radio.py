# GRN stands for Generate Random Number
import psutil
import time

def generate_random_number():
    # Get system metrics
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used  # In bytes
    
    disk_usage = psutil.disk_usage('/')
    used_disk = disk_usage.used  # In bytes

    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0  # In MHz
    current_time = int(time.time())  # Epoch time in seconds
    
    # Combine all factors and generate the "random" number
    custom_random_number = (used_memory + used_disk + int(cpu_freq) + current_time * 1000) % 1000
    return custom_random_number
# GRN stands for Generate Random Number
import psutil
import time

def get_hardware_seed():
    # Get system metrics
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used  # In bytes
    
    disk_usage = psutil.disk_usage('/')
    used_disk = disk_usage.used  # In bytes

    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0  # In MHz
    current_time = int(time.time_ns())  # Epoch time in seconds
    
    io_counters = psutil.disk_io_counters()
    read_bytes = io_counters.read_bytes
    write_bytes = io_counters.write_bytes
    byte_cnt = read_bytes ^ write_bytes

    # Combine all factors and generate the "random" number
    return (used_memory ^ used_disk ^ int(cpu_freq * 1000) ^ current_time ^ byte_cnt) & 0xFFFFFFFFFFFFFFFF
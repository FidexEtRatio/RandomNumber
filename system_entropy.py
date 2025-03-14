# GRN stands for Generate Random Number
import psutil
import time

def xorshift128plus(seed1, seed2):
    s0, s1 = seed1, seed2
    t = s0
    s0 = s1
    s1 = s1 ^ (s1 >> 23) ^ (t ^ (t >> 17) ^ (s0 ^ (s0 >> 26)))
    return s1 + s0

def get_hardware_seed():
    # Get system metrics
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used  # In bytes
    
    disk_usage = psutil.disk_usage('/')
    used_disk = disk_usage.used  # In bytes

    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0  # In MHz
    current_time = int(time.time())  # Epoch time in seconds
    
    io_counters = psutil.disk_io_counters()
    read_bytes = io_counters.read_bytes
    write_bytes = io_counters.write_bytes

    # Combine all factors and generate the "random" number
    custom_random_number = used_memory + used_disk + int(cpu_freq) + read_bytes + write_bytes + current_time
    return xorshift128plus(custom_random_number % (2 ** 64))
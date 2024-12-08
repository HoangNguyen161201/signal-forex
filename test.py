import time

def get_random_number(): 
    current_time = time.time()
    random_number = int(current_time * 1000) % 100000
    return random_number

print(get_random_number())
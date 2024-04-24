import time
import math
import multiprocessing

def is_prime(n):
    """Check if n is prime."""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_max_prime_in_range(min_number, max_number):
    """Finds the largest prime in the given range."""
    max_prime = 0
    for number in range(max_number, min_number - 1, -1):
        if is_prime(number):
            max_prime = number
            break
        if number % 2 == 0:
            number -= 1
    return max_prime

def find_max_prime_parallel(timeout, digits):
    """Finds the largest prime with specified number of digits within timeout using parallel processing."""
    min_number = 10**(digits - 1)
    max_number = (10**digits) - 1
    num_processes = multiprocessing.cpu_count()
    chunk_size = (max_number - min_number + 1) // num_processes

    pool = multiprocessing.Pool(processes=num_processes)
    results = []

    start_time = time.time()

    for i in range(num_processes):
        start = min_number + i * chunk_size
        end = min(min_number + (i + 1) * chunk_size, max_number + 1)
        results.append(pool.apply_async(find_max_prime_in_range, args=(start, end)))

    pool.close()
    pool.join()

    max_prime = max(result.get() for result in results)

    print("Largest prime found within", timeout, "seconds with", digits, "digits:", max_prime)

if __name__ == '__main__':
    find_max_prime_parallel(5, 15)  # Procurar o maior número primo com cerca de 17 dígitos dentro de 5 segundos

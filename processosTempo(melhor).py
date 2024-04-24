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
            return number
        if number % 2 == 0:
            number -= 1
    return max_prime

def find_max_prime_parallel(timeout):
    """Finds the largest prime within the given timeout using parallel processing."""
    start_time = time.time()
    num_processes = multiprocessing.cpu_count()
    max_prime = 0
    increment = 10**12  # Aumenta de 10^7 a cada iteração

    while time.time() - start_time < timeout:
        pool = multiprocessing.Pool(processes=num_processes)
        results = []

        for i in range(num_processes):
            start = max_prime + 1
            end = max_prime + increment
            results.append(pool.apply_async(find_max_prime_in_range, args=(start, end)))

        pool.close()
        pool.join()

        max_prime = max(result.get() for result in results)

    print("Maximum prime found within", timeout, "seconds:", max_prime)

if __name__ == '__main__':
    find_max_prime_parallel(1)  # Procurar o maior número primo possível em 5 segundos

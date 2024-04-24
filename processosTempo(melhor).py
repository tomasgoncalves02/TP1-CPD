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

def find_max_prime_parallel(timeout, num_processes):
    """Finds the largest prime within the given timeout using parallel processing."""
    start_time = time.time()
    max_prime = 0
    increment = 10**14  # Increases by 10^7 at each iteration

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

    num_digits = len(str(max_prime))
    print(f"{num_processes: <12}| {timeout: <5}s | {max_prime: <20} | ({num_digits})")

if __name__ == '__main__':
    print("Nº Processos | Tempo | Maior primo | (nº dígitos)")
    for timeout, num_processes in [(5, 4), (20, 4), (20, 8), (60, 4), (60, 8)]:
        find_max_prime_parallel(timeout, num_processes)

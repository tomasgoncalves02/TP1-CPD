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

def find_max_prime_in_range(min_number, max_number, timeout):
    """Finds the largest prime in the given range within timeout."""
    max_prime = 0
    start_time = time.time()
    for number in range(max_number, min_number - 1, -1):
        if is_prime(number):
            max_prime = number
            if time.time() - start_time >= timeout:
                break
        if number % 2 == 0:
            number -= 1
    return max_prime

def find_max_prime_parallel(timeout, max_digits):
    """Finds the largest prime with up to max_digits within timeout using parallel processing."""
    start_time = time.time()
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    max_prime = 0

    for digits in range(max_digits, 0, -1):
        min_number = 10**(digits - 1)
        max_number = (10**digits) - 1
        chunk_size = (max_number - min_number + 1) // num_processes
        results = []

        for i in range(num_processes):
            start = min_number + i * chunk_size
            end = min(min_number + (i + 1) * chunk_size, max_number + 1)
            results.append(pool.apply_async(find_max_prime_in_range, args=(start, end, timeout / max_digits)))

        pool.close()
        pool.join()

        max_prime = max(result.get() for result in results)

        if time.time() - start_time >= timeout:
            print("Time's up! Maximum prime found within", timeout, "seconds with up to", digits, "digits:", max_prime)
            break

    if time.time() - start_time < timeout:
        print("Maximum prime found within", time.time() - start_time, "seconds with up to", max_digits, "digits:", max_prime)

if __name__ == '__main__':
    find_max_prime_parallel(5, 17)  # Procurar o maior número primo com até 17 dígitos dentro de 5 segundos

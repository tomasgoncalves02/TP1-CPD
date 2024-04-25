import time
import math
import multiprocessing
import threading

# Definição de um semáforo para controlar o acesso concorrente aos resultados
result_semaphore = threading.Semaphore()

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

def find_max_prime_in_range(min_number, max_number, results):
    """Finds the largest prime in the given range."""
    max_prime = 0
    for number in range(max_number, min_number - 1, -1):
        if is_prime(number):
            max_prime = number
            break
    # Utiliza semáforo para controlar o acesso concorrente aos resultados
    with result_semaphore:
        results.append(max_prime)

def find_max_prime_parallel(timeout, num_processes):
    """Finds the largest prime within the given timeout using parallel processing."""
    results = multiprocessing.Manager().list()
    increment = 10**14  # Aumenta de 10^7 a cada iteração

    start_time = time.time()
    while time.time() - start_time < timeout:
        pool = multiprocessing.Pool(processes=num_processes)
        results[:] = []  # Limpa os resultados da iteração anterior

        for i in range(num_processes):
            start = i * increment + 1
            end = (i + 1) * increment
            pool.apply_async(find_max_prime_in_range, args=(start, end, results))

        pool.close()
        pool.join()

        max_prime = max(results)
        increment *= 2  # Dobra o incremento a cada iteração

    num_digits = len(str(max_prime))
    print(f"{num_processes: <12}| {timeout: <5}s | {max_prime: <20} | ({num_digits})")

if __name__ == '__main__':
    print("Nº Processos | Tempo | Maior primo | (nº dígitos)")
    for timeout, num_processes in [(5, 4), (20, 4), (20, 8), (60, 4), (60, 8)]:
        find_max_prime_parallel(timeout, num_processes)

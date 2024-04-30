import time
import math
import multiprocessing

# Definição de um lock para controlar o acesso concorrente aos resultados
result_lock = multiprocessing.Lock()

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

def find_max_prime_in_range(min_number, max_number, max_prime):
    """Finds the largest prime in the given range."""
    current_max_prime = 0
    for number in range(max_number, min_number - 1, -1):
        if is_prime(number) and number > current_max_prime:
            current_max_prime = number
    with result_lock:
        if current_max_prime > max_prime.value:
            max_prime.value = current_max_prime

def find_max_prime_parallel(timeout, num_processes):
    """Finds the largest prime within the given timeout using parallel processing."""
    max_prime = multiprocessing.Value('i', 0)

    start_number = 1
    increment = 10**14  # Inicialização do incremento
    start_time = time.time()
    while time.time() - start_time < timeout:
        pool = multiprocessing.Pool(processes=num_processes)
        max_prime.value = 0  # Reset max_prime for each iteration

        for i in range(num_processes):
            end_number = start_number + increment
            print(f"Processo {i+1}: Intervalo de números: {start_number} - {end_number}")
            pool.apply_async(find_max_prime_in_range, args=(start_number, end_number, max_prime))
            start_number = end_number + 1  # Atualiza o número de início para o próximo intervalo

        pool.close()
        pool.join()

    num_digits = len(str(max_prime.value))
    print(f"{num_processes: <12}| {timeout: <5}s | {max_prime.value: <20} | ({num_digits})")

if __name__ == '__main__':
    print("Nº Processos | Tempo | Maior primo | (nº dígitos)")
    for timeout, num_processes in [(5, 4), (20, 4), (20, 8), (60, 4), (60, 8)]:
        find_max_prime_parallel(timeout, num_processes)

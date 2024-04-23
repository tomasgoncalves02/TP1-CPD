import math
import multiprocessing

def sieve_of_eratosthenes(start, end):
    primes = []
    sieve = [True] * (end + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(math.sqrt(end)) + 1):
        if sieve[i]:
            for j in range(i * i, end + 1, i):
                sieve[j] = False

    for i in range(max(2, start), end + 1):
        if sieve[i]:
            primes.append(i)

    return primes

def find_max_prime_parallel(timeout):
    """Finds the largest prime until timeout using parallel processing."""
    num_processes = multiprocessing.cpu_count()
    processes = []
    results = []

    chunk_size = timeout // num_processes

    for i in range(num_processes):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, timeout)
        process = multiprocessing.Process(target=sieve_of_eratosthenes, args=(start, end))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    for process in processes:
        results.extend(process.return_value)

    max_prime = max(results)
    print(max_prime)

if __name__ == '__main__':
    find_max_prime_parallel(5)  # Exemplo de timeout grande para demonstração

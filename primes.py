import time
import multiprocessing

# Função para verificar se um número é primo
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Função para encontrar o maior primo dentro de um intervalo
def find_max_prime(start, end, result):
    max_prime = 0
    for i in range(start, end):
        if is_prime(i) and i > max_prime:
            max_prime = i
    result.put(max_prime)

# Função para paralelizar a busca por números primos
def parallel_find_max_prime(timeout, num_processes):
    start_time = time.time()
    result = multiprocessing.Queue()
    processes = []
    max_number = num_processes * 1000000  # Defina o maior número do intervalo

    # Calcula os intervalos de forma mais precisa
    interval_size = max_number // (2 * num_processes)
    for i in range(2 * num_processes):
        start = i * interval_size + 1
        end = (i + 1) * interval_size + 1
        if i == 2 * num_processes - 1:  # Para garantir que o último processo alcance o máximo
            end = max_number + 1
        p = multiprocessing.Process(target=find_max_prime, args=(start, end, result))
        processes.append(p)
        p.start()

    # Aguarda todos os processos terminarem ou até o tempo limite ser atingido
    for p in processes:
        p.join(timeout - (time.time() - start_time))

    max_prime = 0
    while not result.empty():
        prime = result.get()
        if prime > max_prime:
            max_prime = prime

    return max_prime

if __name__ == '__main__':
    # Configurações
    timeout = 5  # Tempo limite em segundos
    num_processes = [4, 8]  # Número de processos para paralelização
    timeouts = [5, 20, 60]  # Durações dos timeouts em segundos

    # Imprime cabeçalho da tabela
    print("Nº Processos | Tempo | Maior primo (nº dígitos)")

    # Loop através de diferentes configurações de processos e timeouts
    for np in num_processes:
        for t in timeouts:
            max_prime = parallel_find_max_prime(t, np)
            print(f"{np:<13} | {t}s | {max_prime:<19} ({len(str(max_prime))})")

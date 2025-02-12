import socket
import threading
import random

# Конфігурація сервера
HOST = '192.168.31.197'
PORT = 5556
N = 64

# Функція для обробки клієнта
def handle_client(client_socket, address):
    print(f"Підключено клієнта: {address}")

    # Ініціалізація гри
    balance = N
    guessed_number = random.randint(1, N)
    client_socket.sendall(f"Start. Balance={balance}\n".encode())
    print(f"Загадане число для клієнта {address}: {guessed_number}")

    try:
        while True:
            # Отримання повідомлення від клієнта
            data = client_socket.recv(1024).decode().strip()
            if not data:
                raise ConnectionResetError("Клієнт відключився")

            print(f"Від клієнта {address}: {data}")

            if data == "END":
                client_socket.sendall(f"Loosed. I guessed {guessed_number}\n".encode())
                break

            # Перевірка коректності введення
            try:
                a, b = map(int, data.split())
                if not (1 < a < b < N):
                    raise ValueError
            except ValueError:
                client_socket.sendall("Try again.\n".encode())
                continue

            # Обробка діапазону
            if a == b:  # Якщо введено однакові числа
                if guessed_number == a:  # Якщо загадане число відповідає введеному
                    client_socket.sendall(f"Win! Prize={balance}\n".encode())
                    break
                else:
                    client_socket.sendall(f"Out of range. Balance={balance}\n".encode())
                    balance -= 1  # Можна зменшити баланс за невдалу спробу
            else:
                # Обробка звичайного діапазону
                if a <= guessed_number <= b:
                    client_socket.sendall(f"In range. Balance={balance}\n".encode())
                else:
                    client_socket.sendall(f"Out of range. Balance={balance}\n".encode())

                range_size = b - a + 1
                balance -= range_size

            if balance <= 0:
                client_socket.sendall(f"Loosed. I guessed {guessed_number}\n".encode())
                break

            if a <= guessed_number <= b:
                client_socket.sendall(f"In range. Balance={balance}\n".encode())
            else:
                client_socket.sendall(f"Out of range. Balance={balance}\n".encode())

    except (ConnectionResetError, BrokenPipeError):
        print(f"Клієнт {address} відключився.")
    finally:
        client_socket.close()

# Запуск сервера
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Сервер запущено на {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# Запуск клієнта
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    try:
        while True:
            # Отримання повідомлення від сервера
            response = client.recv(1024).decode().strip()
            print(response)

            if response.startswith("Win") or response.startswith("Loosed"):
                break

            # Введення даних від користувача
            message = input("Введіть діапазон (a b) або END: ").strip()
            client.sendall(message.encode())

            if message == "END":
                break

    except (ConnectionResetError, BrokenPipeError):
        print("З'єднання з сервером втрачено.")
    finally:
        client.close()

if __name__ == "__main__":
    mode = input("Виберіть режим (server/client): ").strip().lower()
    if mode == "server":
        start_server()
    elif mode == "client":
        start_client()
    else:
        print("Невірний режим.")

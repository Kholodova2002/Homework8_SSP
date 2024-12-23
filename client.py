import asyncio
import sys

async def tcp_echo_client(host, port):
    """
    Запускает TCP-клиента, который подключается к серверу, отправляет строки и получает эхо.
    Цикл продолжается до тех пор, пока пользователь не введет 'exit'.
    
    Параметры:
    - host: IP-адрес или доменное имя сервера.
    - port: Порт сервера.
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"[Client] Соединение с сервером {host}:{port} установлено")
    except Exception as e:
        print(f"[Client][ERROR] Не удалось подключиться к серверу {host}:{port}. Ошибка: {e}")
        return

    try:
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            user_input = user_input.strip()
            if not user_input:
                print("[Client][WARNING] Пустая строка не отправляется")
                continue

            writer.write(user_input.encode('utf-8'))
            await writer.drain()
            print(f"[Client] Отправлено на сервер: {user_input}")

            # Прием данных от сервера
            data = await reader.read(1024)
            if not data:
                print("[Client][WARNING] Сервер отключился")
                break

            echoed_message = data.decode('utf-8').strip()
            print(f"[Client] Получено от сервера: {echoed_message}")

            if user_input.lower() == 'exit':
                print("[Client] Завершение работы клиента по команде 'exit'")
                break
    except Exception as e:
        print(f"[Client][ERROR] Произошла ошибка: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("[Client] Соединение с сервером закрыто")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='TCP Echo Client')
    parser.add_argument('--host', type=str, default='localhost', help='IP-адрес сервера')
    parser.add_argument('--port', type=int, default=9090, help='Порт сервера')

    args = parser.parse_args()

    try:
        asyncio.run(tcp_echo_client(args.host, args.port))
    except KeyboardInterrupt:
        print("\n[Client] Завершение работы клиента по запросу пользователя")
        sys.exit(0)

import asyncio
import sys

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[Server] Подключен клиент {addr}")

    while True:
        data = await reader.read(1024)  # Прием данных порциями по 1 КБ
        if not data:
            # Клиент отключился
            print(f"[Server] Клиент {addr} отключился")
            break

        message = data.decode('utf-8').strip()
        print(f"[Server] Получены данные от клиента {addr}: {message}")

        if message.lower() == 'exit':
            print(f"[Server] Клиент {addr} отправил команду 'exit'. Отключение.")
            break

        # Отправка данных обратно клиенту (эхо)
        writer.write(data)
        await writer.drain()
        print(f"[Server] Отправлены данные клиенту {addr}: {message}")

    writer.close()
    await writer.wait_closed()
    print(f"[Server] Соединение с клиентом {addr} закрыто")

async def main(host='0.0.0.0', port=9090):
    """
    Запускает TCP-эхо-сервер.
    
    Параметры:
    - host: IP-адрес для прослушивания (по умолчанию '0.0.0.0' — все интерфейсы).
    - port: Порт для прослушивания (по умолчанию 9090).
    """
    server = await asyncio.start_server(handle_echo, host, port)

    addr = server.sockets[0].getsockname()
    print(f"[Server] Сервер запущен и слушает {addr}")

    async with server:
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            pass  # Обработка отмены задачи при завершении программы

if __name__ == "__main__":
    HOST = '0.0.0.0'  # Слушать на всех интерфейсах
    PORT = 9090        # Вы можете изменить порт при необходимости

    try:
        asyncio.run(main(HOST, PORT))
    except KeyboardInterrupt:
        print("\n[Server] Остановка сервера по запросу пользователя")
        sys.exit(0)
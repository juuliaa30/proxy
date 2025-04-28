import socket
from _thread import start_new_thread
from urllib.parse import urlparse

BLACKLIST_FILE = "blacklist.txt"
BUFFER_SIZE = 8192


def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as file:
            return {line.strip().lower() for line in file if line.strip()}
    except FileNotFoundError:
        return set()


def start_proxy(proxy_ip, proxy_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_ip, proxy_port))
    proxy_socket.listen(5)
    print(f"Прокси-сервер запущен на {proxy_ip}:{proxy_port}")
    while True:
        client_connection, _ = proxy_socket.accept()
        start_new_thread(handle_client_request, (client_connection,))


def handle_client_request(client_connection):
    blocked_domains = load_blacklist()
    target_server_socket = None
    try:
        client_request = client_connection.recv(BUFFER_SIZE)
        if not client_request:
            return

        request_first_line = client_request.split(b'\r\n')[0].decode('latin-1')
        request_components = request_first_line.split()
        if len(request_components) < 3:
            return

        http_method, request_url, http_version = request_components

        url_components = urlparse(request_url)
        if not url_components.netloc:
            return

        target_host = url_components.hostname
        target_port = url_components.port if url_components.port else 80

        if target_host.lower() in blocked_domains:
            error_response = (
                "HTTP/1.1 403 Forbidden\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Connection: close\r\n\r\n"
                "<h1>403 FORBIDDEN</h1><p>Доступ запрещен</p>"
            )
            client_connection.sendall(error_response.encode('utf-8'))
            print(f"{request_url} - 403 Forbidden")
            return

        resource_path = url_components.path if url_components.path else '/'
        if url_components.query:
            resource_path += '?' + url_components.query


        target_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_server_socket.connect((target_host, target_port))

        modified_request = client_request.replace(
            f"{http_method} {request_url} {http_version}".encode(),
            f"{http_method} {resource_path} {http_version}".encode()
        )

        target_server_socket.sendall(modified_request)

        server_response = target_server_socket.recv(BUFFER_SIZE)
        if server_response:
            response_status_line = server_response.split(b'\r\n')[0].decode('latin-1')
            status_parts = response_status_line.split(' ')
            if len(status_parts) >= 2:
                response_code = status_parts[1]
                status_message = ' '.join(status_parts[2:]) if len(status_parts) > 2 else 'OK'
                print(f"{request_url} - {response_code} {status_message}")
            else:
                print(f"{request_url} - 000 Unknown")

            client_connection.sendall(server_response)

            while True:
                try:
                    response_data = target_server_socket.recv(BUFFER_SIZE)
                    if not response_data:
                        break
                    client_connection.sendall(response_data)
                except (socket.error, ConnectionResetError):
                    break

    except Exception as error:
        print(f"Ошибка при обработке запроса: {str(error)}")
    finally:
        client_connection.close()
        if target_server_socket:
            target_server_socket.close()


if __name__ == "__main__":
    start_proxy("127.0.0.2", 8080)
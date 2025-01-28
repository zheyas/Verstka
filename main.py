from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Определяем настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
    Класс, отвечающий за обработку входящих запросов от клиентов.
    """

    def do_GET(self):
        """ Обработка входящих GET-запросов. """
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Определяем путь к запрашиваемому ресурсу
        if self.path == "/":
            requested_path = os.path.join(root_dir, "HTML", "contacts.html")
        elif self.path.startswith("/css"):
            requested_path = os.path.join(root_dir, self.path[1:])  # Удаляем начальный слэш для корректного пути
        else:
            requested_path = os.path.join(root_dir, self.path[1:])

        # Определяем тип контента
        content_type = "text/html"
        if requested_path.endswith(".css"):
            content_type = "text/css"

        # Чтение содержимого файла и отправка ответа
        try:
            with open(requested_path, "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            # Ответ для неизвестных ресурсов
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>404 Not Found</title></head>"
                                   "<body><h1>File Not Found</h1></body></html>", "utf-8"))

    def do_POST(self):
        """ Обработка входящих POST-запросов. """
        content_length = int(self.headers['Content-Length'])  # Длина данных из заголовков
        post_data = self.rfile.read(content_length)  # Данные из тела запроса

        # Печатаем данные в консоль
        print("Received POST data:")
        print(post_data.decode('utf-8'))  # Предполагается, что данные закодированы в UTF-8

        # Ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h2>POST request processed</h2></body></html>")


if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Корректная остановка веб-сервера
    webServer.server_close()
    print("Server stopped.")

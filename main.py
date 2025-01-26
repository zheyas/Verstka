from http.server import BaseHTTPRequestHandler, HTTPServer

# Определяем настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Чтение содержимого HTML-файла
        try:
            with open("HTML/contacts.html", "r", encoding="utf-8") as file:
                html_content = file.read()

            # Отправка содержимого HTML-файла в ответе
            self.wfile.write(bytes(html_content, "utf-8"))
        except FileNotFoundError:
            # Обработка случая, если файл не найден
            self.wfile.write(bytes("<html><head><title>404 Not Found</title></head>"
                                   "<body><h1>File Not Found</h1></body></html>", "utf-8"))

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])  # Получаем длину данных
        post_data = self.rfile.read(content_length)  # Читаем данные из тела запроса

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

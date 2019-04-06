import socketserver

_BUF_SIZE = 1024  # TODO: replace with relevant buffer size (bytes)


class MapHandler(socketserver.BaseRequestHandler):
    """
    Request Handler.
    """
    indexPage = ""

    def handle(self):
        data = self.request.recv(_BUF_SIZE).strip()
        lines = data.splitlines()
        first_line = lines[0]
        first_line_tokens = first_line.decode().split(' ')
        get_values = {}
        if len(first_line_tokens) > 1:
            url = first_line_tokens[1]
            url = url.lower()
            url_tokens = url.split('?')[1:]
            if len(url_tokens) > 0:
                get_tokens = url_tokens[0]
                get_tokens = get_tokens.split('&')
                for token in get_tokens:
                    s = token.split('=')
                    key = s[0]
                    value = s[1]
                    get_values[key] = value
        verb = first_line_tokens[0]
        if verb == 'GET':
            student_id = get_values.get("student_id", None)
            student_name = get_values.get("student_name", None)
            if student_id is not None and student_name is not None:
                info = {
                    "studentId": student_id,
                    "studentName": student_name,
                    "ip": self.client_address[0]
                }
                self._save_info(info)
                response = "Success"
            else:
                response = self.indexPage
            self.request.sendall(response.encode())
        else:
            print("unknown verb, ignoring request {}", data)
            return

    def _save_info(self, info) -> None:
        pass

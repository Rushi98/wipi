import socketserver


class DataViewHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.
    """

    def handle(self):
        data = self.request.recv(1024).strip()
        lines = data.splitlines()
        first_line = lines[0]
        first_line_tokens = first_line.decode().split(' ')
        verb = first_line_tokens[0]
        if verb == 'GET':
            url = first_line_tokens[1]
            url = url.lower()
            url_tokens = url.split('/')[1:]
            print(url_tokens)
            if url_tokens[0] == 'sessions':
                if len(url_tokens) == 1:
                    self.response = self._getsessions()
                else:
                    datetime = url_tokens[1]
                    self.response = self._getsessionattendance(datetime)
            elif url_tokens[0] == 'people':
                self.response = self._getpeople()
            elif url_tokens[0] == 'person' and len(url_tokens) > 1:
                mac = url_tokens[1]
                self.response = self._getpersonattendance(mac)
            else:
                print("unknown path, ignoring request {}", data)
                return
        else:
            print("unknown verb, ignoring request {}", data)
            return
        self.request.sendall(self.response.encode())

    def _getsessions(self):
        return "not yet implemented"

    def _getsessionattendance(self, datetime):
        return "not yet implemented"

    def _getpeople(self):
        return "not yet implemented"

    def _getpersonattendance(self, mac):
        return "not yet implemented"

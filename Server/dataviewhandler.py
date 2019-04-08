import socketserver
from urllib.parse import unquote
from main import indexPage, cursor, mapping, start_scan, stop_scan


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
            url = unquote(url)
            print(url)
            url_tokens = url.split('/')[1:]
            print(url_tokens)
            response = ""
            if url_tokens[0] == 'sessions':
                if len(url_tokens) == 1:
                    response = self._get_sessions()
                else:
                    datetime = url_tokens[1]
                    response = self._get_session_attendance(datetime)
            elif url_tokens[0] == 'people':
                response = self._get_people()
            elif url_tokens[0] == 'person' and len(url_tokens) > 1:
                mac = url_tokens[1]
                response = self._get_person_attendance(mac)
            elif url_tokens[0] == 'startmap':
                self._start_map()
            elif url_tokens[0] == 'stopmap':
                self._stop_map()
            elif url_tokens[0] == 'startscan':
                start_scan()
            elif url_tokens[0] == 'stopscan':
                stop_scan()
            elif mapping:
                get_values = {}
                url_tokens = url.split('?')[1:]
                if len(url_tokens) > 0:
                    get_tokens = url_tokens[0]
                    get_tokens = get_tokens.split('&')
                    for token in get_tokens:
                        s = token.split('=')
                        key = s[0]
                        value = s[1]
                        get_values[key] = value
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
                    response = indexPage
            else:
                print("unknown path, ignoring request {}", data)
                return
        else:
            print("unknown verb, ignoring request {}", data)
            return
        self.request.sendall(str(response).encode())

    def _get_sessions(self):
        query = """select distinct session from ATTENDANCE_DATA order by session;"""
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _get_session_attendance(self, datetime):
        query = """select session, bits_id, name, hits from (select * from ATTENDANCE_DATA AD, STUDENT_INFO SI where 
                    AD.session==? and AD.mac_address==SI.mac_address) as t1 order by bits_id;"""
        try:
            cursor.execute(query, (datetime,))
            rows = cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _get_people(self):
        query = """select bits_id, name, mac_address from STUDENT_INFO order by bits_id;"""
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _get_person_attendance(self, mac):
        query = """select session, hits from ATTENDANCE_DATA where mac_address==?;"""
        try:
            cursor.execute(query, (mac,))
            rows = cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _start_map(self):
        self.mapping = True
        print("Mapping started")
        pass

    def _stop_map(self):
        self.mapping = False
        print("Mapping stopped")
        pass

    def _save_info(self, info):
        query = """INSERT OR IGNORE INTO STUDENT_INFO VALUES ((SELECT mac_address from IP_MAC WHERE ip_address==?), ?, ?);"""
        val = (info["ip"], info["studentName"], info["studentId"])
        try:
            self.cursor.execute(query, val)
        except Exception as e:
            raise e

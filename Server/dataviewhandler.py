import socketserver
import subprocess
from urllib.parse import unquote

class DataViewHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.
    """
    cursor = None

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
            elif url_tokens[0] == 'startMap':
                self._start_map()
            elif url_tokens[0] == 'stopMap':
                self._stop_map()
            elif url_tokens[0] == 'startScan':
                self._start_scan()
            elif url_tokens[0] == 'stopScan':
                self._stop_scan()
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
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _get_session_attendance(self, datetime):
        query = """select session, bits_id, name, hits from (select * from ATTENDANCE_DATA AD, STUDENT_INFO SI where 
                    AD.session==? and AD.mac_address==SI.mac_address) as t1 order by bits_id;"""
        try:
            self.cursor.execute(query, (datetime,))
            rows = self.cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _get_people(self):
        query = """select bits_id, name, mac_address from STUDENT_INFO order by bits_id;"""
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _get_person_attendance(self, mac):
        query = """select session, hits from ATTENDANCE_DATA where mac_address==?;"""
        try:
            self.cursor.execute(query, (mac,))
            rows = self.cursor.fetchall()
        except Exception as e:
            raise e
        else:
            return rows

    def _start_map(self):
        pass

    def _stop_map(self):
        pass

    def _start_scan(self):
        pass

    def _stop_scan(self):
        pass

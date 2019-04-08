import socketserver
import subprocess
import os
from signal import SIGKILL
from urllib.parse import unquote

SCANNING_EXEC = "executor.sh"
SCANNING_DIR = "../Scanning"


class DataViewHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.
    """
    cursor = None

    mapping = False

    map_pid = -1

    scanning = False

    scan_pid = -1

    indexPage = ""

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
                self._start_scan()
            elif url_tokens[0] == 'stopscan':
                self._stop_scan()
            elif self.mapping:
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
                    response = self.indexPage

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
        if self.mapping:
            pass
        n = os.fork()
        if n > 0:
            # parent
            self.map_pid = n
        else:
            subprocess.run([""])
        pass

    def _stop_map(self):
        pass

    def _start_scan(self):
        if self.scanning:
            pass
        n = os.fork()
        if n > 0:
            # parent
            # n = child's pid
            self.scan_pid = n
            self.scanning = True
        else:
            # child
            subprocess.run([SCANNING_EXEC], cwd=SCANNING_DIR)
            print("Scanning started")
        pass

    def _stop_scan(self):
        if self.scanning:
            os.kill(self.scan_pid, SIGKILL)
            self.scanning = False
            self.scan_pid = -1
            print("Scanning stopped")

    def _save_info(self):
        pass
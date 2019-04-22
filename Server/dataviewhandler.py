import socketserver
from typing import List, Dict, Any
from urllib.parse import unquote
from main import indexPage, cursor, mapping, start_scan, stop_scan
import json


def response_ok_header(content_len: int) -> str:
    return "HTTP/1.1 200 OK\n" \
           "Content-Type: text/json\n" \
           "Content-Length: {0}" \
           "\n" \
        .format(content_len)


RESPONSE_BAD: str = "HTTP/1.1 400 Bad Request\n" \
                    "Content-Type: text\n" \
                    "Content-Length: 0"


def _get_people() -> List[Dict[str, object]]:
    query = """select bits_id, name, mac_address from STUDENT_INFO order by bits_id;"""
    res: List[Dict[str, object]] = []
    try:
        cursor.execute(query)
        for row in cursor.fetchall():
            r = {'bits_id': row[0],
                 'name': row[1],
                 'mac_address': str(row[2])}
            res.append(r)
    except Exception as e:
        raise e
    else:
        return res


def _save_info(info: Dict[str, object]) -> None:
    query = """INSERT OR IGNORE 
    INTO STUDENT_INFO 
    VALUES (
        (SELECT mac_address 
            from IP_MAC 
            WHERE ip_address==?), ?, ?
    );"""
    val = (info["ip"], info["studentName"], info["studentId"])
    try:
        cursor.execute(query, val)
    except Exception as e:
        raise e


def _get_person_attendance(mac: str) -> List[Dict[str, Any]]:
    query = """select session, hits from ATTENDANCE_DATA where mac_address==?;"""
    res: List[Dict[str, Any]] = []
    try:
        cursor.execute(query, (mac,))
        for row in cursor.fetchall():
            r = {'session': row[0],
                 'hits': row[1]}
            res.append(r)
    except Exception as e:
        raise e
    else:
        return res


def _get_session_attendance(datetime: str) -> List[Dict[str, Any]]:
    query = """select session, bits_id, name, hits from (select * from ATTENDANCE_DATA AD, STUDENT_INFO SI where 
                AD.session==? and AD.mac_address==SI.mac_address) as t1 order by bits_id;"""
    res: List[Dict[str, Any]] = []
    try:
        cursor.execute(query, (datetime,))
        for row in cursor.fetchall():
            r = {'session': str(row[0]),
                 'bits_id': str(row[1]),
                 'name': str(row[2]),
                 'hits': row[3]
                 }
            res.append(r)
    except Exception as e:
        raise e
    else:
        return res


def _get_sessions() -> List[str]:
    query = """select distinct session from ATTENDANCE_DATA order by session;"""
    res: List[str] = []
    try:
        cursor.execute(query)
        for row in cursor.fetchall():
            res.append(str(row[0]))
    except Exception as e:
        raise e
    else:
        return res


class DataViewHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.
    """

    def handle(self):
        data: bytearray = self.request.recv(1024).strip()
        lines: List[bytearray] = data.splitlines()
        first_line: bytearray = lines[0]
        first_line_tokens: List[str] = first_line.decode().split(' ')
        verb = first_line_tokens[0]
        if verb == 'GET':
            url: str = first_line_tokens[1]
            url = url.lower()
            url = unquote(url)
            print(url)
            url_tokens: List[str] = url.split('/')[1:]
            print(url_tokens)
            response: Any = None
            if url_tokens[0] == 'sessions':
                if len(url_tokens) == 1:
                    response = json.dumps(_get_sessions())
                else:
                    datetime = url_tokens[1]
                    response = json.dumps(_get_session_attendance(datetime))
            elif url_tokens[0] == 'people':
                response = json.dumps(_get_people())
            elif url_tokens[0] == 'person' and len(url_tokens) > 1:
                mac = url_tokens[1]
                response = json.dumps(_get_person_attendance(mac))
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
                    _save_info(info)
                    response = "Success"
                else:
                    response = indexPage
            else:
                print("unknown path, ignoring request {}", data)
                return
        else:
            print("unknown verb, ignoring request {}", data)
            return
        if response is None:
            self.request.sendall(RESPONSE_BAD)
        else:
            response = "{0}\n".format(str(response))
            response = "{0}{1}".format(response_ok_header(len(response)), str(response))
            self.request.sendall(response.encode())

    def _handle_get(self, first_line_tokens: List[str]):
        pass

    def _start_map(self):
        self.mapping = True
        print("Mapping started")
        pass

    def _stop_map(self):
        self.mapping = False
        print("Mapping stopped")
        pass

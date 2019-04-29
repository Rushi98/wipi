import os
import sqlite3
import subprocess
from typing import Dict, List

LIB_DIR: str = os.environ['WIPI_LIB_DIR']  # exported by `wipi`
DB_NAME: str = f'{LIB_DIR}/rpi.db'


def save_student_info(info: Dict[str, str]) -> None:
    ip: str = info['ip']
    student_name: str = info['studentName']
    student_id: str = info['studentId']
    mac: str = ''

    arp_op = subprocess.check_output(['arp', ip]).decode()
    arp_info = parse_arp_output(arp_op)
    for info in arp_info:
        if info['Address'] == ip:
            mac = info['HWaddress']
            break
    print(str(arp_info))
    print(mac)
    if mac == '':
        raise Exception('bad state',
                        f"couldn't find mac address corresponding to ip {ip}")

    query = """INSERT OR REPLACE 
    INTO STUDENT_INFO 
    (mac_address, name, bits_id)
    VALUES (
        ?, ?, ?
    );"""
    val = (mac, student_name, student_id)
    try:
        connection: sqlite3.Connection = sqlite3.connect(DB_NAME)
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute(query, val)
        connection.commit()
        connection.close()
    except Exception as e:
        raise e


def parse_arp_output(arp_op: str) -> List[Dict[str, str]]:
    """
        parses output table of `arp` to list of objects
        assumptions:
            1. first row of the output is key row
    """
    rows = arp_op.split('\n')
    key_row = rows[0].split()
    data_rows = rows[1:]
    ans = []
    for data_row in data_rows:
        data = {}
        data_row = data_row.split()
        for i in range(len(data_row)):
            data[key_row[i]] = data_row[i]
        ans.append(data)
    return ans

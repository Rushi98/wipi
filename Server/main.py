#!/usr/bin/env python
import socketserver
from signal import SIGKILL
from typing import Type

import dataviewhandler
import os
import subprocess


if 'WIPI_LIB_DIR' not in os.environ:
    print("Program files not found. exiting.")
    exit(0)

LIB_DIR: str = os.environ['WIPI_LIB_DIR']  # exported by `wipi`

DB_NAME: str = f'{LIB_DIR}/rpi.db'
INDEX_HTML: str = f'{LIB_DIR}/register.html'
SCANNING_EXEC: str = f'{LIB_DIR}/executor.sh'

PORT: int = 80  # TODO: use port passed by argument

map_pid: int = -1

scanning: bool = False

scan_pid: int = -1

if __name__ == "__main__":
    from dataviewhandler import DataViewHandler
    requestHandler: Type[DataViewHandler] = dataviewhandler.DataViewHandler
    with socketserver.TCPServer(("", PORT), requestHandler) as httpd:
        try:
            print("Serving at port ", PORT)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down ... ")
            httpd.shutdown()
            print("Done")


def start_scan():
    global scanning
    if scanning:
        pass
    n = os.fork()
    if n > 0:
        # parent
        # n = child's pid
        global scan_pid
        scan_pid = n
        scanning = True
    else:
        # child
        subprocess.run([SCANNING_EXEC], shell=True)
        print("Scanning started")
    pass


def stop_scan():
    global scanning
    global scan_pid
    if scanning:
        os.kill(scan_pid, SIGKILL)
        scanning = False
        scan_pid = -1
        print("Scanning stopped")

#!/bin/python
import socketserver
from _signal import SIGKILL

import dataviewhandler
import os
import sqlite3
import subprocess

PORT = 80
DB_NAME = 'rpi.db'
INDEX_HTML = "register.html"
SCANNING_EXEC = "executor.sh"

cursor = None

mapping = False

map_pid = -1

scanning = False

scan_pid = -1

indexPage = ""

if __name__ == "__main__":
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    requestHandler = dataviewhandler.DataViewHandler
    requestHandler.cursor = cursor
    index_page = open(INDEX_HTML, "r")
    requestHandler.indexPage = index_page.read()
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

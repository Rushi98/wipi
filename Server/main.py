#!/bin/python
import socketserver
import dataviewhandler
import sqlite3

PORT = 80
DB_NAME = '../rpi.db'
INDEX_HTML = "register.html"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
requestHandler = dataviewhandler.DataViewHandler
requestHandler.cursor = cursor

if __name__ == "__main__":
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

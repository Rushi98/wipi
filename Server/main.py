#!/bin/python
import socketserver
import dataviewhandler
import sqlite3

PORT = 80
DB_NAME = 'wipi.db'

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
Handler = dataviewhandler.DataViewHandler
Handler.cursor = cursor

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            print("Serving at port ", PORT)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down ... ")
            httpd.shutdown()
            print("Done")

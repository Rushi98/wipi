#!/bin/python
import socketserver
import dataviewhandler

PORT = 80

Handler = dataviewhandler.DataViewHandler

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            print("Serving at port ", PORT)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down ... ")
            httpd.shutdown()
            print("Done")

#!/bin/python
import socketserver
import maphandler

PORT = 80
INDEX_HTML = "register.html"

requestHandler = maphandler.MapHandler

if __name__ == "__main__":
    index_page = open(INDEX_HTML, "r")
    requestHandler.indexPage = index_page.read()
    with socketserver.TCPServer(("", PORT), requestHandler) as server:
        try:
            print("[Map] Serving at port ", PORT)
            server.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down ...")
            server.shutdown()
            print("Done")
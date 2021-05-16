# https://docs.python.org/3/howto/sockets.html
# https://stackoverflow.com/questions/8627986/how-to-keep-a-socket-open-until-client-closes-it
# https://stackoverflow.com/questions/10091271/how-can-i-implement-a-simple-web-server-using-python-without-using-any-libraries


from socket import *
import os
from os import path
from pprint import pprint

def render_template(template_name="index.html",vars=""):
    html_str = ""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = path.join(root_dir,template_name)
    with open(template_path, 'r') as f:
        html_str = f.read()
        # html_str = html_str.format(**vars)
    # print (html_str)
    return html_str


def app():
    vars = {'filename':"app2.html", 'data':[1,2,3,4,5,6,6]}
    return render_template("app2.html", vars)
def style():
    return render_template("styles.css")

def favicon():
    return render_template("favicon.html")

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        # serversocket.bind(('localhost', 9000))
        serversocket.bind(('dpk-basicserver.herokuapp.com', 9000))
        # 5 represents number of connections allowed in waiting queue
        serversocket.listen(5)
        while(1):
            # This is blocking call. unless client make connection flow stays here
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")
            # pprint ("resding request")
            # pprint (rd)
            # pprint ("read request complete")
            if (len(pieces) > 0):
                print(pieces[0])
                # following 3 lines makes HTTP header.
                # Headers are required to communicate with browser over HTTP protocol
                # They are as per RFC standards
                data1 = "HTTP/1.1 200 OK\r\n"
                # data going across the socket is always nedds to be in utf-8 format
                # data1 += "Content-Type: text/{MIME}; charset=utf-8\r\n"
                # # a single blank line in compulsory to tell header ends here.
                # data1 += "\r\n"
                url =  pieces[0].split(" ")[1]
                # print (url)
                if url == '/': # home page
                    data1 += "Content-Type: text/html; charset=utf-8\r\n"
                    # a single blank line in compulsory to tell header ends here.
                    data1 += "\r\n"
                    data1+= app()
                    # print (data1)

                elif url == '/favicon.ico':
                    data1 += "Content-Type: text/html; charset=utf-8\r\n"
                    # a single blank line in compulsory to tell header ends here.
                    data1 += "\r\n"
                    data1 += favicon()

                elif url == "/styles.css":
                    data1 += "Content-Type: text/css; charset=utf-8\r\n"
                    # a single blank line in compulsory to tell header ends here.
                    data1 += "\r\n"
                    data1 += style()
                else:
                    data1 += "Content-Type: text/html; charset=utf-8\r\n"

                    data1 += "404 page not found"

                # here you can see  GET /favicon.ico HTTP/1.1 which is call from browser
                # following 3 lines makes HTTP header.
                # Headers are required to communicate with browser over HTTP protocol
                # They are as per RFC standards
                # data1 = "HTTP/1.1 200 OK\r\n"
                # # data going across the socket is always nedds to be in utf-8 format
                # data1 += "Content-Type: text/html; charset=utf-8\r\n"
                # # a single blank line in compulsory to tell header ends here.
                # data1 += "\r\n"

            # this encoding is required as data is in unicode in python but it needs to be in utf-8 while sending over the socket
            print ("finale data")
            print (data1)
            print ("finale data")
            clientsocket.sendall(data1.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        print("\nShutting down...\n")
        serversocket.shutdown(SHUT_RDWR)
        serversocket.close()
        print("\nProcess complete\n")
    except Exception as exc:
        raise
        print("Error:\n")
        print(exc)

    # shutdown will shut it down from all process using it
    # close will close it for only current process calling it
    # close is compulsory after shutdown to free resources allocated to socket
    # serversocket.shutdown(SHUT_RDWR)
    serversocket.close()

print ('Access http://localhost:9000')
createServer()

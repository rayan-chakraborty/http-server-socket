import socket
import os

def get_content(name):
    if name == '':
        name = 'index'
    file_name = os.getcwd()+'\\Static\\'+name+'.html'
    file_obj = open(file_name,'r')
    content = file_obj.read()
    return content

def GetName(request):
    try:
        name = request.split('\n')[0].split()[1]
        name = name[1:]
    except:
        name = ''
    return name

def GetHttp(code):
    return "HTTP/1.0 {} OK\n\n".format(code)

def GetResponse(request):
    name = GetName(request)
    content = get_content(name)
    response_text = GetHttp(200) + content
    response = response_text.encode()
    return response


def init_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 1234
    sock.bind(('localhost',port))
    print("Connection started at http://127.0.0.1:{}/".format(port))
    sock.listen(1)
    return sock


def runserver():
    sock = init_socket()
    while True:
        client, addr = sock.accept()
        try:
            request = client.recv(1024).decode()
            print("Client is connected at address", addr)
            print("Requested URL {}".format(GetName(request)))
            response = GetResponse(request)
            client.sendall(response)
            client.close()
        except KeyboardInterrupt:
            break
        except Exception as e:
            name = GetName(request)
            if name == 'favicon.ico':
                continue
            print(e)
            response = "{} <h1>Sorry this page {} doesn't exist in our website</h1>".format(GetHttp(200),name)
            client.sendall(response.encode())
            client.close()
    sock.close()


if __name__ == "__main__":
    runserver()

    
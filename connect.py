import socket

host = '127.0.0.1'
port = 13854
param = '{"enableRawOutput": false, "format": "Json"}'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
    skt.connect((host, port))
    
    skt.sendall(str.encode(param))
    print('response: ' + skt.recv(2048).decode('utf-8'))

    while True:
        data = skt.recv(2048)
        if not data: 
            print('no data')
            break

        with open('output_mindwave.txt', 'a') as file:
            file.write(data.decode('utf-8'))
            print(data.decode('utf-8'))
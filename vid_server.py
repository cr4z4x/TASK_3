import socket, cv2, pickle,struct

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip="192.168.111.167"
print('HOST :',host_ip)



# Socket Bind
server_socket.bind(("192.168.111.167",5167))

# Socket Listen
server_socket.listen(10)
print("LISTENING")

# Socket Accept
while True:
    clien_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM:',addr)
    if clien_socket:
        vid = cv2.VideoCapture(0)
        
        while(vid.isOpened()):
            img,frame = vid.read()
            pd = pickle.dumps(frame)        #pickeled data
            message = struct.pack("Q",len(pd))+pd  #here the Q is pd long long int it its about 4 bytes
            clien_socket.sendall(message)  #the first 8 bytes here are for the amout of frame data
            
            cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('/'):
                clien_socket.close()
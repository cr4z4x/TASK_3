import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.111.167' #serveer ip

client_socket.connect((host_ip,5167))
data = b""
data_len_indicator = struct.calcsize("Q")
while True:
    while len(data) < data_len_indicator:
        packet = client_socket.recv(6) # taking in 4 B at at time beacuse its the max amount
        data+=packet
    frame_size = data[:data_len_indicator]
    data = data[data_len_indicator:]    #currently no data    #taking all data fater the frame size indiactor which is the frame data
    msg_size = struct.unpack("Q",frame_size)[0] #returns tuple with the data given

    while len(data) < msg_size:
        data += client_socket.recv(4096)            #recieving frame data
    frame_data = data[:msg_size]
    data  = data[msg_size:]                         #resetting data to 0
    frame = pickle.loads(frame_data)                #unpickeling the data Bytes----->nparray
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('/'):
        break
client_socket.close()
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 8300))
players_address_carts = [[] for kk in range(3)]
carts = [[] for k in range(3)]
while True:
    data, address = server.recvfrom(1024)
    data = data.decode('utf-8').split()
    if data[0] == "leave":
        carts[int(data[8])][players_address_carts[int(data[8])].index(address)] = ['leave', data[1], data[2]]
        print(f"{address} leave server")
        continue
    if address not in players_address_carts[int(data[7])]:
        players_address_carts[int(data[7])].append(address)
        carts[int(data[7])].append([0, 0, 0, 0, 0, 0, 0, 0])
        print(f"{address}" + " connect to server")
    carts[int(data[7])][players_address_carts[int(data[7])].index(address)] = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]]
    data_for_send = ''
    for t in range(len(carts[int(data[7])])):
        if players_address_carts[int(data[7])][t] != address:
            if carts[int(data[7])][t][0] == 'leave':
                data_for_send += f'leave {carts[int(data[7])][t][1]} {carts[int(data[7])][t][2]}  '
            else:
                data_for_send += f'{carts[int(data[7])][t][0]} {carts[int(data[7])][t][1]} {carts[int(data[7])][t][2]} {carts[int(data[7])][t][3]} {carts[int(data[7])][t][4]} {carts[int(data[7])][t][5]} {carts[int(data[7])][t][6]} {carts[int(data[7])][t][7]} {carts[int(data[7])][t][8]}  '
    server.sendto(data_for_send.encode('utf-8'), address)

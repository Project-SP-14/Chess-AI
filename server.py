import socket
import threading

clients = []

def handle_client(conn, player_id):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            # forward the move to the other client
            for i, c in enumerate(clients):
                if i != player_id:
                    c.send(data.encode())

        except:
            break

    conn.close()
    clients[player_id] = None

def main():
    host = "0.0.0.0"
    port = 5050

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)

    print("Server waiting for players...")

    while len(clients) < 2:
        conn, addr = server.accept()
        clients.append(conn)
        print("Player connected:", addr)
        t = threading.Thread(target=handle_client, args=(conn, len(clients)-1))
        t.start()

    print("Two players connected. Match started.")

if __name__ == "__main__":
    main()

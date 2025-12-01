import socket
import threading

class ClientConnection:
    def __init__(self, host, port, board):
        self.host = host
        self.port = port
        self.board = board
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((host, port))
            print("Connected to server")
        except:
            print("Could not connect to server")
            return

        t = threading.Thread(target=self.listen_for_moves)
        t.daemon = True
        t.start()

    # send local move to server
    def send_move(self, x1, y1, x2, y2):
        msg = f"{x1},{y1},{x2},{y2}"
        try:
            self.socket.send(msg.encode())
        except:
            print("Failed to send move")

    # receive opponent moves
    def listen_for_moves(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break

                parts = data.split(",")
                x1 = int(parts[0])
                y1 = int(parts[1])
                x2 = int(parts[2])
                y2 = int(parts[3])

                print("Opponent moved:", data)

                # apply move to board
                self.board.apply_network_move(x1, y1, x2, y2)

            except:
                break

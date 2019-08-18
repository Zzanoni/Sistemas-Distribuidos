import java.io.*;
import java.net.*;

public class Oserver{

    public static void main (String args[]) throws Exception{

        DatagramSocket serverSocket = new DatagramSocket();
        byte[] recBuffer = new byte[1024];
        byte[] sendBuffer = new byte[1024];

        while(true){
            DatagramPacket recPacket = new DatagramPacket(recBuffer,
                                                          recBuffer.length);
            serverSocket.receive(recPacket);
            String informacao = new String(recPacket.getData(),
                                            recPacket.getOffset(),
                                            recPacket.getLength());//pq iso
            InetAddress IPAddress = recPacket.getAddress();
            int port = recPacket.getPort();
            sendBuffer = "Sou o servidor".getBytes();
            DatagramPacket sendPacket = new DatagramPacket(sendBuffer,
                                                            sendBuffer.length,
                                                            IPAddress,
                                                            port);
            serverSocket.send(sendPacket);
        }
        //serverSocket.close();
    }
}

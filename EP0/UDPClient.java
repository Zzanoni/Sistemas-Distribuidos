import java.io.*;
import java.net.*;
import java.util.Scanner;

public class client{

    public static void main (String args[]) throws IOException {
        while(true){
            BufferedReader inFromUser = new BufferedReader(new InputStreamReader(
    				System.in));
            InetAddress IPAddress = InetAddress.getByName("127.0.0.1");
            DatagramSocket clientSocket = new DatagramSocket();
            byte[] sendData = new byte[1024];
            Scanner scan = new Scanner(System.in);
            String msg = inFromUser.readLine();
            sendData = msg.getBytes();
            DatagramPacket sendPacket =
                new DatagramPacket(sendData, sendData.length, IPAddress, 9877);
                                                                        //Porta
            //Envio da mensagem
            clientSocket.send(sendPacket);
            //Recebimento da resposta do server
            byte[] recBuffer = new byte[1024];
            DatagramPacket recPacket = new DatagramPacket(recBuffer,
                                                          recBuffer.length);
            clientSocket.receive(recPacket);
            String resposta = new String(recPacket.getData());
            System.out.println(resposta);
            clientSocket.close();
        }
    }
}

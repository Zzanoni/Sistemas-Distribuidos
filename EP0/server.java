import java.io.*;
import java.net.*;

class server {

	public static void main(String args[]) throws Exception {

		DatagramSocket serverSocket = new DatagramSocket(9877);
		byte[] receiveData = new byte[1024];
		byte[] sendData = new byte[1024];
		String cliente1=null, cliente2=null;
		String[] buffer1 = new String[100];
		String[] buffer2 = new String[100];
		int proxMsg1=1, proxMsg2=1;
		while (true) {
			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length);
			serverSocket.receive(receivePacket);

			String sentence = new String(receivePacket.getData());

			//Separa a mensagem em tokens
			String[] partes = sentence.split("\\|");

			//Atribui cada token a sua variavel
			String nomClient = partes[0];
			Integer numMsg = Integer.valueOf(partes[1]);
			String msg = partes[2];
			System.out.println("Mensagem "+numMsg+" recebida do "+nomClient);

			//Criacao e verificacao dos buffers
			if(cliente1==null)
				cliente1=nomClient;
			if(cliente1.equals(nomClient)){
				cliente1 = nomClient;
				if(proxMsg1==numMsg){
					buffer1[proxMsg1-1] = msg;
					proxMsg1++;
					sendData = "\nRecebida com sucesso!\n".getBytes();
					System.out.println("\nMensagem "+numMsg+" recebida com sucesso."+
										"\nArmazenando no buffer do "+nomClient+"...\n");
				}
				else if(proxMsg1>numMsg){
					sendData = ("\nMensagem duplicada!\nO pacote "+numMsg+
								" ja foi recebido.\n").getBytes();
					System.out.println("\nMensagem duplicada!\n");
				}
				else{
					sendData = ("\nMensagem fora de ordem!\nO pacote "+
								proxMsg1+" não foi recebido.\n").getBytes();
					System.out.println("\nMensagem fora de ordem!\n");
				}
			}
			else{
				cliente2 = nomClient;
				if(proxMsg2==numMsg){
					buffer2[proxMsg2-1] = msg;
					proxMsg2++;
					sendData = "\nPacote recebido com sucesso!\n".getBytes();
					System.out.println("\nMensagem "+numMsg+" recebida com sucesso."+
										"\nArmazenando no buffer do "+nomClient+"...\n");
				}
				else if(proxMsg2>numMsg){
					sendData = ("\nMensagem duplicada!\nO pacote "+numMsg+
								" ja foi recebido.\n").getBytes();
					System.out.println("\nMensagem duplicada!\n");
				}
				else{
					sendData = ("\nMensagem fora de ordem!\nO pacote "+
								proxMsg2+" nao foi recebido.\n").getBytes();
					System.out.println("\nMensagem fora de ordem!\n");
				}
			}

			//Envia a msg para o cliente
			InetAddress IPAddress = receivePacket.getAddress();
			int port = receivePacket.getPort();
			DatagramPacket sendPacket = new DatagramPacket(sendData,
					sendData.length, IPAddress, port);
			serverSocket.send(sendPacket);
		}
	}
}

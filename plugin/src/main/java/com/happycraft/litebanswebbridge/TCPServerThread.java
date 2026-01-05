// TCPServerThread.java
package com.happycraft.litebanswebbridge;

import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class TCPServerThread extends Thread {
    private final LitebansWebBridge plugin;
    private final int port;
    private volatile boolean running = true;
    private ServerSocket serverSocket;

    public TCPServerThread(LitebansWebBridge plugin, int port) {
        this.plugin = plugin;
        this.port = port;
    }

    @Override
    public void run() {
        try {
            serverSocket = new ServerSocket(port, 50, InetAddress.getByName("127.0.0.1"));
            plugin.getLogger().info("TCP server started, listening on localhost:" + port + "...");
            while (running) {
                Socket clientSocket = serverSocket.accept();
                new ClientHandler(clientSocket, plugin).start();
            }
        } catch (IOException e) {
            plugin.getLogger().severe("TCP server error: " + e.getMessage());
        }
    }

    public void shutdown() {
        running = false;
        try {
            if (serverSocket != null) serverSocket.close();
        } catch (IOException ignored) {}
    }
}

package com.happycraft.litebanswebbridge;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class ClientHandler extends Thread {
    private final Socket socket;
    private final LitebansWebBridge plugin;

    public ClientHandler(Socket socket, LitebansWebBridge plugin) {
        this.socket = socket;
        this.plugin = plugin;
    }

    @Override
    public void run() {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                plugin.getLogger().info("Received message: " + line);
                if (line.toLowerCase().startsWith("unban ")) {
                    String username = line.substring(6).trim();
                    plugin.runUnbanCommand(username);
                }
                // More commands can be extended here
            }
        } catch (IOException e) {
            plugin.getLogger().warning("Client connection error: " + e.getMessage());
        } finally {
            try { socket.close(); } catch (IOException ignored) {}
        }
    }
}
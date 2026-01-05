// LitebansWebBridge.java
package com.happycraft.litebanswebbridge;

import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;

public class LitebansWebBridge extends JavaPlugin {
    private TCPServerThread tcpServerThread;

    @Override
    public void onEnable() {
        tcpServerThread = new TCPServerThread(this, 3024); // Listen on port 3024
        tcpServerThread.start();
        getLogger().info("LitebansWebBridge plugin enabled, TCP server listening on port: 3024");
    }

    @Override
    public void onDisable() {
        if (tcpServerThread != null) {
            tcpServerThread.shutdown();
        }
        getLogger().info("LitebansWebBridge plugin disabled");
    }

    // Safely execute commands on the main thread from the TCP thread
    public void runUnbanCommand(String username) {
        Bukkit.getScheduler().runTask(this, () -> {
            Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "unban " + username + " -s User self-service unblocking from web");
            getLogger().info("Executed unban command for: " + username);
        });
    }
}

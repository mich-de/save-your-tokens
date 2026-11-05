# 16. Android as Network Proxy

When your network (hotel Wi-Fi, corporate firewall, etc.) blocks AI services, route traffic through an Android phone.

## Architecture

```
[PC] --USB tethering--> [Android phone] --VPN--> [Home gateway] --> Internet
```

The phone acts as both a network adapter (USB tethering) and a VPN endpoint. The PC's AI tools route through the phone, which tunnels everything to your home network via VPN.

## Setup

### 1. Phone side

- Connect the phone to the PC via USB.
- Enable **USB tethering** (Settings > Connections > Mobile Hotspot and Tethering > USB tethering).
- Activate a VPN connection to your home gateway (IPSec, WireGuard, or OpenVPN — whatever your router supports).
- The phone gets a VPN IP on the home network (e.g., `192.168.x.201`).

### 2. PC side

- The USB tethering interface appears as a network adapter.
- Set the proxy environment variable to route through the phone:
  ```
  HTTP_PROXY=http://127.0.0.1:8080
  HTTPS_PROXY=http://127.0.0.1:8080
  ```
- Or configure your AI tools to use the tethered connection directly.

### 3. What routes through the phone

Only AI/dev tools that need unblocked access:
- Claude Code
- OpenCode
- Other AI coding agents

Regular browsing can stay on the local Wi-Fi.

## Verifying the setup

```bash
# Check your public IP (should be your home IP, not the hotel's)
curl.exe -s https://api.ipify.org

# Ping the home gateway through the VPN
ping 192.168.x.1
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `curl.exe` shows hotel IP | VPN not active on phone, or tethering not routing through VPN |
| PowerShell `Invoke-WebRequest` bypasses proxy | Known Windows PS 5.1 bug — use `curl.exe` instead |
| Gateway blocks TR-064 from PC | TR-064 calls must go from the phone, not the PC |
| VPN drops during IP rotation | Wait for reconnect, verify tunnel restored |

## ADB utilities

If the phone has `adb` debugging enabled, you can automate tasks:

```bash
# Forward a local port to the phone
adb forward tcp:8080 tcp:8080

# Run a command on the phone
adb shell <command>

# Check the phone's VPN interface
adb shell ip addr show ipsec0
```

## Security notes

- Keep file and script names generic on both devices (see [13-network-and-naming.md](13-network-and-naming.md)).
- The phone's VPN credentials stay on the phone — never copy them to the PC.
- USB tethering is more secure than Wi-Fi hotspot (no radio interception).

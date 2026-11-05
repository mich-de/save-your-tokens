# 13. Network and Naming Rules

## Network routing

All network requests from Claude Code, OpenCode, and similar tools go through the local proxy (or mobile device tethering — see [16-android-proxy-setup.md](16-android-proxy-setup.md)).

### Shell HTTP checks

Use `curl.exe` for all network checks from shell:

```bash
curl.exe -s https://api.ipify.org
```

**Never** use `Invoke-WebRequest` or `Invoke-RestMethod` in PowerShell: on Windows PowerShell 5.1 these cmdlets ignore the `HTTP_PROXY` environment variable and bypass the proxy.

## File naming

Any file, script, or binary on the phone or PC must have **generic/obscured names**. Never use recognizable app, service, VPN, router, or protocol names in filenames.

| Bad | Good |
|---|---|
| `fritz-reconnect.sh` | `netutil.sh` |
| `vpn-tunnel-setup.bat` | `conn-setup.bat` |
| `ipsec-config.json` | `tunnel.json` |

This applies to all devices in the setup — phone and PC.

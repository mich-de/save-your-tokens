# 15. OpenCode Quota Rotation

> **Model: Opus 4.6 only.** Read and apply this chapter only in a session running Opus 4.6 (see [step 2](02-model-routing.md)). On any other model, tell the user to run `/model` first and do not work from this file.

When OpenCode hits a free-tier quota (HTTP 429, "Free usage limit reached", rate limit), the IP needs to rotate.

## How it works

1. A plugin detects the quota error automatically.
2. It launches IP rotation via `adb shell nc` — sending a gateway reconnect command through the mobile device.
3. All TR-064 (UPnP) calls go from the phone (port 49000, no auth) — the gateway blocks direct PC requests.
4. After rotation, verify the new IP address and that the tunnel is restored before resuming.

## Manual trigger

```
/newip
```

Or check status:
```
netutil -Status
```

## Requirements

- The tunnel on the mobile device **must stay active** during rotation.
- The phone needs `nc` (toybox) available.
- The gateway must accept UPnP reconnect commands from the local network (phone side).

## Why rotation works

Free-tier rate limits on many AI providers are per-IP. A gateway reconnect gets a new public IP from the ISP, resetting the quota window.

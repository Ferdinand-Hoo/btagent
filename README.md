# BTAgent

AI-powered Bluetooth diagnostic agent for Linux and automotive systems.

BTAgent automatically analyzes Bluetooth logs (HCI / btmon / bluetoothd) and helps developers quickly locate protocol issues.

## Features

* Analyze HCI logs
* Detect Bluetooth connection failures
* Diagnose A2DP / AVRCP issues
* Generate diagnostic reports

## Example

Input:

```
hci.log
```

Output:

```
ACL connection established
AVRCP SetAbsoluteVolume rejected

Reason:
Target device does not support absolute volume
```

## Architecture

```
User
 │
AI Agent
 │
MCP Server
 │
Skills
 ├── Log Fetcher
 ├── HCI Parser
 └── Protocol Analyzer
```

## Roadmap

### v0.1

* HCI log parser
* Basic AI analysis

### v0.2

* AVRCP analyzer
* A2DP analyzer

### v0.3

* SSH log collection
* MCP integration

### v1.0

* Full Bluetooth diagnostic agent

## Use cases

* Automotive Bluetooth debugging
* Linux Bluetooth stack development
* Protocol troubleshooting

## License

MIT


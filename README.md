# Network Automation Project



## Requirements
- Configure IPv4 addresses on devices in VLANs across both sites ("Customer Office" and "Data Center").
- Set up IPv4 WAN interfaces, ensuring correct subnetting.
- Implement Port-Channel configurations using PAGP (Customer Office) and LACP (Data Center).
- Configure RSTP and HSRP for optimal network performance and load balancing.
- Set up RIPv2 on routers.
- Configure default static routes and HSRP on the WAN side.
- Set up DHCP pools and ensure clients receive IP addresses dynamically.
- Apply security measures, including port security and STP security features.
- Verify network connectivity across all devices.

## Project Structure
- main.py
- config.json
- class Devices(mosteniri->)
            -__init__.py
            -devices.py
            -router.py
            -switch.py
- ssh_manager.py
- configuration.py
- utilis.py(decoratorii)
- README.md
# Project Documentation 
## 1. Overview
This project provides an automated configuration system for network devices like routers and switches. It enables the automated provisioning of network devices based on predefined configurations stored in JSON format. The main components of this system include Python classes representing network devices, configuration loading utilities, SSH management for applying configurations, and logging mechanisms to monitor execution.

## 2. Core Components
- 2.1 Devices Class (Base Class)
The Devices class is the base class for all network devices, such as routers and switches. It contains common attributes like:

hostname: Name of the device.
ip: IP address of the device.
device_type: Type of the device (router or switch).
config: The configuration details of the device, passed in as a dictionary parsed from a JSON file.
- 2.2 Router Class
The Router class inherits from the Devices class and represents router-specific configuration capabilities. It provides functionality for:

Configuring interfaces with IP addresses and subnet masks.
Applying OSPF routing protocol configurations.
Configuring RIPv2, DHCP, and HSRP (Hot Standby Router Protocol).
Managing the router's network operations through methods that dynamically generate configuration commands.
- 2.3 Switch Class
The Switch class also inherits from Devices and handles the configuration of network switches. This includes:

VLAN configuration and creation.
Default gateway setup.
RSTP (Rapid Spanning Tree Protocol) for preventing network loops.
Port security configurations, ensuring limited MAC addresses on access ports.
Port channel aggregation (EtherChannel) for bundling multiple links.
## 3. Configuration Files
The system reads device configurations from a JSON file. Each device, either a router or a switch, has a unique configuration, which includes:

Interface definitions with IP and subnet mask details.
Routing protocols like OSPF or RIPv2.
Additional services like DHCP, HSRP, and port security (for switches).
Example (from config.json):

```
{
  "devices": [
    {
      "hostname": "R1",
      "ip": "192.168.1.2",
      "type": "router",
      "config": {
        "interfaces": [
          { "name": "g0/0", "ipv4": "192.168.1.2", "sm": "255.255.255.0" }
        ],
        "ospf": { "process_id": 1, "networks": [{ "network": "192.168.1.0", "wildcard_mask": "0.0.0.255", "area": 0 }] },
        "dhcp": { "pool": "192.168.1.100 192.168.1.200", "default_router": "192.168.1.2" },
        "hsrp": { "interface": "g0/0", "group": 1, "virtual_ip": "192.168.1.1", "priority": 120 }
      }
    }
  ]
}
```
## 4. SSH Manager
The system includes an SSH manager that connects to network devices and applies the generated configuration commands via SSH sessions. The key functionality involves:

Establishing a secure SSH connection.
Sending configuration commands to devices.
Handling authentication and error reporting.
## 5. Utility Functions
- 5.1 Logging
The logging system (logging.basicConfig) is configured to output detailed information about the execution of the scripts, including errors and execution time, making the process of debugging and tracking easier.

- 5.2 Configuration Loader
The load_config() function is responsible for reading JSON configuration files from disk and returning the configuration as a Python dictionary.

```
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
```
## 6. Example Workflow
Define Configuration: The configuration for routers and switches is stored in config.json.
Load Configuration: Using load_config(), the configurations are parsed into Python objects.
Create Device Objects: Devices like routers and switches are instantiated using the Router or Switch classes.
Generate Commands: The configure() method is invoked on each device, generating configuration commands.
SSH Connection: The SSH manager connects to the devices and applies the configuration commands.
Log Output: Logging captures each step's status for auditing and troubleshooting.
## 7. Conclusion
This project efficiently automates the configuration of routers and switches in a network environment, minimizing manual errors and maximizing consistency. By leveraging JSON configuration files and dynamic command generation, the system allows scalable network automation across various devices.




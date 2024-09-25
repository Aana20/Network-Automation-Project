from devices.Devices import Device  # Importing the Devices class

class Router(Device):  # Inheriting the parameters of the base class
    def __init__(self, hostname, ip, device_type, config):
        super().__init__(hostname, ip, device_type, config)
    def configure(self):  # Function for configuring the router
        commands = [f"enable\nadmin\nconfigure terminal\n"]  # List of commands that will be executed on the router

        # Configuring the interfaces
        for interface in self.config.get('interfaces', []):  # Take from the config variable of the class, access the JSON file, and iterate through the content
            # Add each command to my list of commands
            commands.append(f"interface {interface['name']}\nip address {interface['ipv4']} {interface['sm']}\nno shutdown\nexit\n")

        # Configuring OSPF
        if 'ospf' in self.config:
            commands.append(f"router ospf {self.config['ospf']['process_id']}\n")
            for network in self.config['ospf']['networks']:
                commands.append(f" network {network['network']} {network['wildcard_mask']} area {network['area']}\n")
            commands.append(f"exit\n")


        # Configuring RIPv2
        if 'rip'  in self.config:
            commands.append("router rip\nversion 2\n")
            for network in self.config['rip']['networks']:
                commands.append(f" network {network['network']}\n")
            commands.append(f"exit\n")

        # Configuring HSRP
        if 'hsrp'  in self.config:
            commands.append(f"interface {self.config['hsrp']['interface']}\n")
            commands.append(f"standby {self.config['hsrp']['group']} ip {self.config['hsrp']['virtual_ip']}\n")
            commands.append(f"standby {self.config['hsrp']['group']} priority {self.config['hsrp']['priority']}\n")
            commands.append(f"standby {self.config['hsrp']['group']} preempt\n")
            commands.append(f"exit\n")

        # Configuring DHCP
        if 'dhcp'  in self.config:
            commands.append(f"ip dhcp pool {self.hostname}_pool\n")
            commands.append(f"network {self.config['dhcp']['pool']}\n")
            commands.append(f"default-router {self.config['dhcp']['default_router']}\n")
            commands.append(f"exit\n")
        return commands

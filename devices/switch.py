from devices.Devices import Device

class Switch(Device):
    def __init__(self, hostname, ip, device_type, config):
        super().__init__(hostname, ip, device_type, config)

    def configure(self):
        commands = [f"enable\nadmin\nconfigure terminal\n"]

        # VLAN Configuration
        if 'vlans' in self.config:
            for vlan in self.config['vlans']:
                commands.append(f"vlan {vlan['id']}\nname {vlan['name']}")

        # VLAN Creation
        if 'create_vlans' in self.config:
            for vlan in self.config['create_vlans']:
                commands.append(f"vlan {vlan['id']}\nname {vlan['name']}\nexit")
                commands.append(f"interface vlan{vlan['id']}\nip address {vlan['ipv4']} {vlan['sm']}\n")
                commands.append(f"no shutdown\nexit\n")

        # Default Gateway Configuration
        if 'default_gateway' in self.config:
            commands.append(f"ip default-gateway {self.config['default_gateway']}\n")

        # RSTP Configuration
        commands.append("spanning-tree mode rapid-pvst")

        # Port-Channel Configuration
        if 'port_channels' in self.config:
            for port_channel in self.config['port_channels']:
                # Format the interfaces correctly as "GigabitEthernetX/X, GigabitEthernetX/X"
                interfaces = ', '.join([f"GigabitEthernet{iface}" for iface in port_channel['interfaces']])
                commands.append(f"interface range {interfaces}\n")
                commands.append(f"channel-group {port_channel['number']} mode {port_channel['mode']}\nexit")
                commands.append(f"interface Port-channel{port_channel['number']}\nexit\n")

        # Port Security Configuration
        if 'port_security' in self.config and self.config['port_security']['enabled']:
            # Apply port security to access ports
            if 'access_ports' in self.config:
                access_ports = ', '.join([f"GigabitEthernet{iface}" for iface in self.config['access_ports']])
                commands.append(f"interface range {access_ports}\n")
                commands.append(f"switchport mode access\n")
                commands.append(f"switchport port-security\n")
                commands.append(f"switchport port-security maximum {self.config['port_security']['max_mac']}\n")
                commands.append(f"switchport port-security violation {self.config['port_security']['violation_mode']}\nexit\n")

        return commands

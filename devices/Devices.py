"""
The Devices class, which will serve as the base class, contains: name, IP, type of device, and the configuration that will be applied.
"""
class Device:
    def __init__(self,hostname,ip,device_type,config):
        self.hostname = hostname
        self.ip = ip
        self.device_type = device_type
        self.config = config
    def __repr__(self):
        return f"{self.device_type.capitalize()}({self.hostname}, {self.ip})"
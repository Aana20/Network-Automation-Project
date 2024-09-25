import subprocess
from ssh_manager import SSHConnection
from devices.router import Router
from devices.switch import Switch
from time import sleep

def verify_connectivity(ip):
    """Ping the device to verify connectivity."""
    try:
        # Adjust the ping count and wait time if needed
        response = subprocess.call(['ping', '-c', '3', ip], stdout=subprocess.DEVNULL)
        return response == 0
    except Exception as e:
        print(f"Ping failed: {e}")
        return False


def configure_device(device: Router or Switch):
    # Get SSH instance
    ssh = SSHConnection.get_instance(device.hostname, device.ip)

    # Open a shell session
    shell = ssh.invoke_shell()

    # Get commands from the device configuration
    commands = device.configure()
    print(commands)

    # Send commands to the shell interactively
    for command in commands:
        sleep(0.25)
        print(f"Current command: {command}")
        shell.send(command + '\n')  # Send the command to the shell
        sleep(0.25)  # Wait for the command to be processed

        # Read and print the output from the shell
        while shell.recv_ready():
            output = shell.recv(1024).decode('utf-8')
            print(output)

    # Save the configuration
    shell.send("exit\n")
    shell.send("write memory\n")
    sleep(1)

    # Read and print the output from the "write memory" command
    while shell.recv_ready():
        output = shell.recv(1024).decode('utf-8')
        print(output)


def configure_devices(devices: Router or Switch):
    for device in devices:
        configure_device(device)  # Call the function to configure each device
        if verify_connectivity(device.ip):  # Verify connectivity
            print(f"Connectivity to {device.hostname} ({device.ip}) is successful.")
        else:
            print(f"Connectivity to {device.hostname} ({device.ip}) failed.")



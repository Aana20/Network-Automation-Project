import paramiko
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SSHConnection:
    _instances = {}

    @staticmethod
    def get_instance(hostname, ip, username='admin', secret='admin', retries=10, delay=5):
        """
        Get an SSH connection instance with retries if the connection fails.
        Arguments:
        - hostname: The hostname of the device.
        - ip: The IP address of the device.
        - username: SSH username (default: 'admin').
        - secret: SSH password (default: 'admin').
        - retries: Number of retry attempts (default: 10).
        - delay: Time in seconds to wait between retries (default: 5 seconds).
        """
        if ip not in SSHConnection._instances:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Attempt to connect with retries
            for attempt in range(retries):
                try:
                    logging.info(f"Attempting to connect to {hostname} ({ip}), attempt {attempt + 1}")
                    client.connect(ip, username=username, password=secret)
                    logging.info(f"Connected to {hostname} ({ip})")
                    SSHConnection._instances[ip] = client
                    return SSHConnection._instances[ip]  # Return on successful connection
                except paramiko.SSHException as e:
                    logging.error(f"Attempt {attempt + 1} to connect to {hostname} ({ip}) failed: {e}")
                    if attempt < retries - 1:  # Only wait if there are more attempts left
                        logging.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)  # Wait before retrying

            # Raise an exception if all retries failed
            raise Exception(f"Failed to connect to {hostname} ({ip}) after {retries} retries")

    @staticmethod
    def close_connections():
        """
        Close all SSH connections.
        """
        for client in SSHConnection._instances.values():
            client.close()
        SSHConnection._instances.clear()  # Clear the dictionary after closing connections
        logging.info("Closed all SSH connections")

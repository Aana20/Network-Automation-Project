from multiprocessing import Queue, Process
from devices.router import Router
from devices.switch import Switch
from configuration import configure_device
from utilis import load_config
from ssh_manager import SSHConnection



def configure_device_wrapper(device, queue):
    """
    Wrapper function to configure the device, ensure SSH connections are closed,
    and send the result to the queue.
    """
    result = {}
    try:
        configure_device(device)
        result['device'] = device.hostname
        result['status'] = 'success'
    except Exception as e:
        result['device'] = device.hostname
        result['status'] = 'failure'
        result['error'] = str(e)
    finally:
        SSHConnection.close_connections()

    # Put the result in the queue to communicate with the main process
    queue.put(result)


def main():
    # Load configuration from the JSON file
    config = load_config('config.json')
    devices = []

    # Create instances of Router and Switch from the config
    for d in config['devices']:
        if d['type'] == 'router':
            devices.append(Router(d['hostname'], d['ip'], d['type'], d['config']))
        elif d['type'] == 'switch':
            devices.append(Switch(d['hostname'], d['ip'], d['type'], d['config']))

    # Create a queue for inter-process communication
    queue = Queue()

    # Create and start processes for each device
    processes = []
    for device in devices:
        process = Process(target=configure_device_wrapper, args=(device, queue))
        processes.append(process)
        process.start()

    # Collect results from the queue
    for process in processes:
        process.join()  # Wait for each process to complete

    # Retrieve results from the queue
    while not queue.empty():
        result = queue.get()
        print(f"Device {result['device']} configuration: {result['status']}")
        if result['status'] == 'failure':
            print(f"Error: {result.get('error')}")


if __name__ == '__main__':
    main()

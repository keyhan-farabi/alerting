import psutil
import time
import yaml
import logging

logging.basicConfig(filename='threshold_monitoring.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def load_config():
    with open("threshold_config.yaml", "r") as stream:
        return yaml.safe_load(stream)

def monitor_ram_usage():
    ram = psutil.virtual_memory()
    total_ram = ram.total
    used_ram = ram.used
    ram_percent = int((used_ram / total_ram) * 100)

    config = load_config()
    ram_threshold = config["ram_threshold"]
    monitor_ram_interval = config["monitor_ram_interval"]

    if ram_percent >= ram_threshold:
        logging.info("RAM Percent: {}%".format(ram_percent))

    time.sleep(monitor_ram_interval)

def monitor_cpu_usage():
    cpu_percent = int(psutil.cpu_percent(interval=1))

    config = load_config()
    cpu_threshold = config["cpu_threshold"]
    monitor_cpu_interval = config["monitor_cpu_interval"]

    if cpu_percent >= cpu_threshold:
        logging.info("CPU Percent: {}%".format(cpu_percent))

    time.sleep(monitor_cpu_interval)

def monitor_network_traffic():
    config = load_config()
    network_interface = config["network_interface"]
    in_threshold = config["network_traffic_threshold"]["in"]
    out_threshold = config["network_traffic_threshold"]["out"]
    monitor_network_interval = config["monitor_network_interval"]

    while True:
        network_stats = psutil.net_io_counters(pernic=True)[network_interface]
        in_bytes = network_stats.bytes_recv
        out_bytes = network_stats.bytes_sent

        if in_bytes >= in_threshold or out_bytes >= out_threshold:
            logging.info("Network Traffic Exceeded Threshold: {} bytes received, {} bytes sent".format(in_bytes, out_bytes))

        time.sleep(monitor_network_interval)

def monitor_swap_usage():
    config = load_config()
    swap_threshold = config["swap_threshold"]
    monitor_swap_interval = config["monitor_swap_interval"]

    while True:
        swap = psutil.swap_memory()
        swap_percent = swap.percent

        if swap_percent >= swap_threshold:
            logging.info("Swap Percent: {}%".format(swap_percent))

        time.sleep(monitor_swap_interval)

def monitor_system():
    config = load_config()
    run_ram_monitor = config.get("run_ram_monitor", False)
    run_cpu_monitor = config.get("run_cpu_monitor", False)
    run_network_monitor = config.get("run_network_monitor", False)
    run_swap_monitor = config.get("run_swap_monitor", False)

    while run_ram_monitor or run_cpu_monitor or run_network_monitor or run_swap_monitor:
        if run_ram_monitor:
            monitor_ram_usage()
            config = load_config()
            run_ram_monitor = config.get("run_ram_monitor", False)

        if run_cpu_monitor:
            monitor_cpu_usage()
            config = load_config()
            run_cpu_monitor = config.get("run_cpu_monitor", False)

        if run_network_monitor:
            monitor_network_traffic()
            config = load_config()
            run_network_monitor = config.get("run_network_monitor", False)

        if run_swap_monitor:
            monitor_swap_usage()
            config = load_config()
            run_swap_monitor = config.get("run_swap_monitor", False)

monitor_system()

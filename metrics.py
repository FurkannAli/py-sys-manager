from socket import recv_fds
import psutil
import time

_last_net_time = None
_last_net_bytes = None

def core_stats():
    cpu_percent = psutil.cpu_percent(interval=0.1)

    cpu_percore_percent = psutil.cpu_percent(interval=None, percpu=True)

    memory = psutil.virtual_memory()

    swap = psutil.swap_memory()

    process_count = len(psutil.pids())

    return{
        "cpu": cpu_percent,
        "cpu_cores": cpu_percore_percent,
        "ram": memory.percent,
        "ram_used": memory.used,
        "ram_total": memory.total,
        "swap": swap.percent,
        "swap_used": swap.used,
        "swap_total": swap.total,
        "processes": process_count
    }

def disk_stats():
    disks = []
    for part in psutil.disk_partitions(all=False):
        if part.fstype in ('', 'tmpfs', 'squashfs', 'devtmpfs'):
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "percent": usage.percent,
                "used": usage.used,
                "total": usage.total
            })
        except (PermissionError, FileNotFoundError):
            continue
        return disks

def net_stats():
    global _last_net_time, _last_net_bytes

    current_time = time.time()
    current_bytes = psutil.net_io_counters()

    if current_bytes is None or _last_net_bytes is None or _last_net_time is None:
        _last_net_time = current_time
        _last_net_bytes = current_bytes
        return {"sent_speed": 0, "recv_speed": 0}

    elapsed = current_time - _last_net_time
    if elapsed <= 0:
        elapsed = 1.0

    sent_speed = (current_bytes.bytes_sent - _last_net_bytes.bytes_sent) / elapsed 
    recv_speed = (current_bytes.bytes_recv - _last_net_bytes.bytes_recv) / elapsed

    _last_net_time = current_time
    _last_net_bytes = current_bytes

    return {
        "sent_speed": max(0, sent_speed),
        "recv_speed": max(0, recv_speed)
    }

def running_procs():
    proc_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pinfo = proc.info
            proc_list.append(f"[{pinfo['pid']}] {pinfo['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return sorted(proc_list)

def hardware_stats():
    temps = {}
    try:
        raw_temps = psutil.sensors_temperatures()
        if raw_temps:
            core_counter = 0

            for sensor_name, entries in raw_temps.items():

                if sensor_name in ('acpitz', 'spd5118'):
                    continue

                #OOMGG I CANT BELIEVE IM DOING THIS AUUUGHGHGHH
                #its fun tho
                for entry in entries:
                    label = entry.label or sensor_name
                    if 'nvme' in sensor_name:
                        display_name = f"Storage ({label})"
                    elif sensor_name == 'coretemp':
                        if 'Package' in label:
                            display_name = "Cpu Package Temp"
                        else:
                            display_name = f"CPU Core {core_counter}"
                            core_counter += 1
                    else:
                        display_name = f"{sensor_name} ({label})"

                    temps[display_name] = {
                        "current": entry.current,
                        "high": entry.high,
                        "crticial": entry.critical
                    }
    except (AttributeError, NotImplementedError):
        #unsupported os/hardware
        pass

    fans = {}
    try:
        raw_fans = psutil.sensors_fans()
        if raw_fans:
            for fan_name, entries in raw_fans.items():
                for entry in entries:
                    label = entry.label or fan_name
                    fans[f"{fan_name} ({label})"] = entry.current
    except (AttributeError, NotImplementedError):
        pass
    
    battery = None
    try:
        raw_batt = psutil.sensors_battery()
        if raw_batt:
            battery = {
                "percent": raw_batt.percent,
                "secsleft": raw_batt.secsleft,
                "power_plugged": raw_batt.power_plugged
            }
    except (AttributeError, NotImplementedError):
        pass

    return {
        "temperatures": temps,
        "fans": fans,
        "battery": battery
    }

if __name__ == "__main__":
    print(core_stats())
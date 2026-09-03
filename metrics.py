import psutil, time
import platform, json, csv

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
            for sensor_name, entries in raw_temps.items():

                if sensor_name in ('acpitz', 'spd5118'):
                    continue

                if sensor_name == 'coretemp':
                    def get_hw_core_num(e):
                        digits = ''.join(filter(str.isdigit, e.label or ''))
                        return int(digits) if digits else 999
                    entries = sorted(entries, key=get_hw_core_num)
                
                core_counter = 0

                #idkkk
                for entry in entries:
                    label = entry.label or sensor_name
                    if 'nvme' in sensor_name:
                        display_name = f"Storage ({label})"
                    elif sensor_name == 'coretemp':
                        if 'Package' in label:
                            display_name = "Cpu Package Temp"
                        else:
                            display_name = f"{core_counter:02d} - HW {label}"
                            core_counter += 1
                    else:
                        display_name = f"{sensor_name} ({label})"

                    temps[display_name] = {
                        "current": entry.current,
                        "high": entry.high,
                        "critical": entry.critical
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

def system_overview():
    boot_time = psutil.boot_time()
    uptime_secs = int(time.time() - boot_time)

    hours, remainder = divmod(uptime_secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    os_info = f"{platform.system()} {platform.release()}"
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    os_info = line.split("=")[1].strip().strip('"')
                    break
    except Exception:
        pass

    cpu_model = platform.processor()
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    cpu_model = line.split(":")[1].strip()
                    break
    except Exception:
        pass

    return{
        "os": os_info,
        "kernel": platform.release(),
        "uptime": uptime_str,
        "cpu_model": cpu_model or "Unknown CPU"
    }

def export_metrics_snapshot(filepath: str, export_format: str = "json"):
    c_stats = core_stats()
    hw_stats = hardware_stats()
    procs = running_procs()

    snapshot_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": system_overview(),
        "core_stats": c_stats,
        "hardware_stats": hw_stats,
        "running_processes": procs
    }

    if export_format.lower() == "json":
        with open(filepath, "w") as f:
            json.dump(snapshot_data, f, indent=4)
    elif export_format.lower() == "csv":
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Metric", "Value"])
            writer.writerow(["System", "OS", snapshot_data["system"]["os"]])
            writer.writerow(["System", "Uptime", snapshot_data["system"]["uptime"]])
            writer.writerow(["System", "CPU Model", snapshot_data["system"]["cpu_model"]])
            writer.writerow(["Core", "CPU Usage (%)", c_stats["cpu"]])
            writer.writerow(["Core", "RAM Usage (%)", c_stats["ram"]])
            writer.writerow(["Core", "Swap Usage (%)", c_stats["swap"]])
            for sensor, val in hw_stats["temperatures"].items():
                writer.writerow(["Temperature", sensor, f"{val['current']}°C"])
            for proc in procs:
                writer.writerow(["Process", "Running", proc])

if __name__ == "__main__":
    print(core_stats())
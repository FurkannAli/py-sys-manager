import psutil

def system_call():
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

def running_procs():
    proc_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pinfo = proc.info
            proc_list.append(f"[{pinfo['pid']}] {pinfo['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return sorted(proc_list)

if __name__ == "__main__":
    print(system_call())
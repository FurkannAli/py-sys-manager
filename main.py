from os import stat
from typing import Container
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QProgressBar
from sys_main import Ui_MainWindow
import sys, psutil, time
from metrics import core_stats, disk_stats, net_stats, running_procs, hardware_stats
import pyqtgraph as pg

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dashboard)

        self.current_interval_ms = 1000
        self.timer.start(self.current_interval_ms)

        self.pushButton_SaveSettings.clicked.connect(self.apply_settings)

        self.pushButton_Refresh.clicked.connect(self.refresh_proc_list)
        self.refresh_proc_list()

        self.pushButton_Kill.clicked.connect(self.kill_proc)

        self.lineEdit_Search.textChanged.connect(self.search_func)

        self.sensor_labels = {}

        #individual core progress bar stuff
        self.core_prog_bars = []
        inital_cores = psutil.cpu_percent(interval=None, percpu=True)
        for i, val in enumerate(inital_cores):
            bar = QProgressBar()
            bar.setRange(0,100)
            bar.setValue(int(val))
            bar.setFormat(f"Core {i}: {val:.1f}%")

            self.gridLayout_Core.addWidget(bar)
            self.core_prog_bars.append(bar)
        
        stats = core_stats()  
        total_ram = format_bytes(stats['ram_total'])
        self.label_mem.setText(f"{self.label_mem.text()} ({total_ram})")
        total_swap = format_bytes(stats["swap_total"])
        self.label_Swap.setText(f"{self.label_Swap.text()} ({total_swap})")

        #a cleaner time and graph thingie
        self.max_secs = 60.0
        self.start_time = time.time()

        self.time_his = []
        self.cpu_his = []
        self.ram_his = []
        self.net_sent_his = []
        self.net_recv_his = []



        self.CPUchart = pg.PlotWidget()
        self.CPUchart.setBackground('k')
        self.CPUchart.setTitle("CPU Usage History", color="w", size="15pt")
        self.CPUchart.setYRange(0,100)
        self.CPUchart.showGrid(x=True, y=True)
        self.cpu_curve = self.CPUchart.plot(self.cpu_his, pen=pg.mkPen(color='r', width=2))
        self.CPUchart.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)

        self.RAMchart = pg.PlotWidget()
        self.RAMchart.setBackground('k')
        self.RAMchart.setTitle("RAM Usage History", color="w", size="15pt")
        self.RAMchart.setYRange(0, 100)
        self.RAMchart.showGrid(x=True, y=True)
        self.ram_curve = self.RAMchart.plot(self.ram_his, pen=pg.mkPen(color='b', width=2))
        self.RAMchart.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)

        self.verticalLayout_ChartThing.addWidget(self.CPUchart)
        self.verticalLayout_ChartThing.addWidget(self.RAMchart)

        #this disk stuff probably doesnt work.. gotta try with other partitions and stuff...
        #disk stuff
        self.disk_bars = {}
        disks = disk_stats() or []

        for disk in disks:
            mount = disk['mountpoint']
            label = QLabel(f"Disk {mount}:")
            bar = QProgressBar()
            bar.setRange(0, 100)
            self.verticalLayout_Disks.addWidget(label)
            self.verticalLayout_Disks.addWidget(bar)
            self.disk_bars[mount] = bar
        
        #net stuff
        self.NetChart = pg.PlotWidget()
        self.NetChart.setBackground('k')
        self.NetChart.setTitle("Network I/O whatevertf (KB/s btw)", color="w", size="15pt")
        self.NetChart.showGrid(x=True, y=True)
        self.NetChart.addLegend(offset=(10, 10))
        self.sent_curve = self.NetChart.plot(self.net_sent_his, pen=pg.mkPen(color='g', width=2), name="Up")
        self.recv_curve = self.NetChart.plot(self.net_recv_his, pen=pg.mkPen(color='c', width=2), name="Down")
        self.verticalLayout_NetStuff.addWidget(self.NetChart)

        #dicts for dynamic temp ui
        self.temp_bars = {}
        self.fan_labels = {}
        self.battery_bar = None
        self.battery_label = None

        self.init_hardware_ui()



    def update_dashboard(self):
        stats = core_stats()
        diskstats = disk_stats() or []
        netstats = net_stats()

        hw = hardware_stats()

        cpu_value = stats['cpu']
        ram_value = stats['ram']
        swap_value = stats['swap']

        #self.label_cpu.setText(str(stats['cpu'])+"%")
        #self.label_mem.setText(str(stats['ram'])+"%")

        self.progressBar_1.setFormat(f"{cpu_value:.1f}%")
        self.progressBar_1.setValue(cpu_value)

        used_ram = format_bytes(stats['ram_used'])
        self.progressBar_2.setFormat(f"{ram_value:.1f}% ({used_ram})")
        self.progressBar_2.setValue(ram_value)

        used_swap = format_bytes(stats["swap_used"])
        self.progressBar_Swap.setFormat(f"{swap_value:.1f}% ({used_swap})")
        self.progressBar_Swap.setValue(swap_value)


        for i, core_val in enumerate(stats['cpu_cores']):
            if i < len(self.core_prog_bars):
                bar = self.core_prog_bars[i]
                bar.setValue(int(core_val))
                bar.setFormat(f"Core {i}: {core_val:.1f}%")

        for disk in diskstats:
            mount = disk['mountpoint']
            if mount in self.disk_bars:
                used_fmt = format_bytes(disk['used'])
                total_fmt = format_bytes(disk['total'])
                self.disk_bars[mount].setValue(int(disk['percent']))
                self.disk_bars[mount].setFormat(f"{disk['percent']:.1f}% ({used_fmt} / {total_fmt})")
        
        #graph things
        now = time.time() - self.start_time
        sent_kb = netstats['sent_speed'] / 1024
        recv_kb = netstats['recv_speed'] / 1024

        self.time_his.append(now)
        self.cpu_his.append(cpu_value)
        self.ram_his.append(ram_value)
        self.net_sent_his.append(sent_kb)
        self.net_recv_his.append(recv_kb)

        cutoff = now - self.max_secs
        while self.time_his and self.time_his[0] < cutoff:
            self.time_his.pop(0)
            self.cpu_his.pop(0)
            self.ram_his.pop(0)
            self.net_sent_his.pop(0)
            self.net_recv_his.pop(0)

        self.cpu_curve.setData(self.time_his, self.cpu_his)
        self.ram_curve.setData(self.time_his, self.ram_his)
        self.sent_curve.setData(self.time_his, self.net_sent_his)
        self.recv_curve.setData(self.time_his, self.net_recv_his)

        if hw["temperatures"]:
            for sensor_id, data in hw["temperatures"].items():
                curr_temp = data["current"]
                print(f"Sensor {sensor_id}: {curr_temp}°C")

        if hw["battery"]:
            batt = hw["battery"]
            status = "Plugged In" if batt["power_plugged"] else "Discharging"
            print(f"Battery: {batt["percent"]}% ({status})")

        hw = hardware_stats()

        for sensor_id, bar in self.temp_bars.items():
            if sensor_id in hw["temperatures"]:
                curr_temp = hw["temperatures"][sensor_id]["current"]
                bar.setValue(int(curr_temp))
                bar.setFormat(f"{curr_temp:.1f}°C")
        
        for fan_id, label in self.fan_labels.items():
            if fan_id in hw["fans"]:
                rpm = hw["fans"][fan_id]
                label.setText(f"{rpm} RPM")

        if self.battery_bar and hw["battery"]:
            batt = hw["battery"]
            status = "Plugged In" if batt["power_plugged"] else "Discharging"
            self.battery_bar.setValue(int(batt["percent"]))
            self.battery_bar.setFormat(f"{batt["percent"]:.0f}% ({status})")
        

        print(f"Refreshed stats: {stats}")

    def init_hardware_ui(self):
        hw = hardware_stats()
        row = 0

        if hw["temperatures"]:
            def sort_key(item):
                name = item[0]
                digits = ''.join(filter(str.isdigit, name))
                return (0, int(digits)) if 'Core' in name and digits else (1, name)
            sorted_temps = sorted(hw["temperatures"].items(), key=sort_key)

            for sensor_id, data in sorted_temps:
                label = QLabel(f"{sensor_id}:")
                bar = QProgressBar()
                bar.setRange(0, 100)
                bar.setFormat("%v°C")
                
                self.gridLayout_Temps.addWidget(label, row, 0)
                self.gridLayout_Temps.addWidget(bar, row, 1)
                self.temp_bars[sensor_id] = bar
                row += 1

            if hw["fans"]:
                for fan_id in hw["fans"]:
                    label_title = QLabel(f"{fan_id}:")
                    label_val = QLabel("0 RPM")

                    self.gridLayout_Temps.addWidget(label_title, row, 0)
                    self.gridLayout_Temps.addWidget(label_val, row, 1)
                    self.fan_labels[fan_id] = label_val
                    row += 1

        if hw["battery"]:
            self.battery_label = QLabel("Battery:")
            self.battery_bar = QProgressBar()
            self.battery_bar.setRange(0, 100)

            self.gridLayout_Temps.addWidget(self.battery_label, row, 0)
            self.gridLayout_Temps.addWidget(self.battery_bar, row, 1)
            row += 1

    def refresh_proc_list(self):
        self.listWidget.clear()
        processes = running_procs()
        self.listWidget.addItems(processes)
        print(f"Loaded {len(processes)} processes into list.")

    def kill_proc(self):
        selected_item = self.listWidget.currentItem()
        if not selected_item:
            print("nothing is selected duuhh")
            return
        
        item_text = selected_item.text()
        try:
            pid_str = item_text.split('[')[1].split(']')[0]
            pid = int(pid_str)

            p = psutil.Process(pid)
            p.terminate()

            print(f"Successfully terminated process PID {pid}")

            self.refresh_proc_list()
        
        except (IndexError, ValueError):
            print("couldnt parse pid from selected item duuhh")
        except psutil.NoSuchProcess:
            print("bro i cant terminate this without root access xx")

    def apply_settings(self):
        self.current_interval_ms = self.spinBox_Interval.value() * 1000
        self.timer.setInterval(self.current_interval_ms)

    def search_func(self):
        search_term = self.lineEdit_Search.text().lower()

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            item_text = item.text().lower()

            if search_term in item_text:
                item.setHidden(False)
            else:
                item.setHidden(True)

def format_bytes(byte_value):
    #mb = byte_value / (1024 * 1024)
    mb = byte_value / 1048576
    if mb >= 1024:
        gb = mb / 1024
        return f"{gb:.2f} GB"
    else:
        return f"{mb:.1f} MB"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
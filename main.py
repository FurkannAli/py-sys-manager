from typing import Container
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar
import psutil
from sys_main import Ui_MainWindow
import sys
from metrics import system_call, running_procs
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

        self.core_prog_bars = []
        inital_cores = psutil.cpu_percent(interval=None, percpu=True)
        for i, val in enumerate(inital_cores):
            bar = QProgressBar()
            bar.setRange(0,100)
            bar.setValue(int(val))
            bar.setFormat(f"Core {i}: {val:.1f}%")

            self.gridLayout_Core.addWidget(bar)
            self.core_prog_bars.append(bar)
        
        stats = system_call()  
        total_ram = format_bytes(stats['ram_total'])
        self.label_mem.setText(f"{self.label_mem.text()} ({total_ram})")
        total_swap = format_bytes(stats["swap_total"])
        self.label_Swap.setText(f"{self.label_Swap.text()} ({total_swap})")


        self.max_his = 60
        self.cpu_his = [0.0] * self.max_his
        self.ram_his = [0.0] * self.max_his

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


    def update_dashboard(self):
        stats = system_call()

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

        self.cpu_his.pop(0)
        self.cpu_his.append(stats['cpu'])
        self.cpu_curve.setData(self.cpu_his)

        self.ram_his.pop(0)
        self.ram_his.append(stats['ram'])
        self.ram_curve.setData(self.ram_his)


        for i, core_val in enumerate(stats['cpu_cores']):
            if i < len(self.core_prog_bars):
                bar = self.core_prog_bars[i]
                bar.setValue(int(core_val))
                bar.setFormat(f"Core {i}: {core_val:.1f}%")

        print(f"Refreshed stats: {stats}")

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
import psutil
import GPUtil
import time
from datetime import datetime
import os


def key_or_val(li, key, value, header):
    if header:
        li.append(key)
    else:
        li.append(value)


def main():
    start = datetime.now().timestamp()
    with open("host_gpu_metrics.log", "a") as f_gpu, open(
        "host_sys_metrics.log", "a"
    ) as f_sys:
        f_gpu.write(
            "timestamp,id,uuid,load,memoryUtil,memoryTotal,memoryUsed,memoryFree,driver,name,serial,display_mode,display_active\n"
        )
        write_sys_metrics(f_sys, first=True)
        i = 0
        while True:
            ts = datetime.now().timestamp()
            for gpu in GPUtil.getGPUs():
                id = gpu.id
                uuid = gpu.uuid
                load = gpu.load
                memoryUtil = gpu.memoryUtil
                memoryTotal = gpu.memoryTotal
                memoryFree = gpu.memoryFree
                driver = gpu.driver
                name = gpu.name
                serial = gpu.serial
                display_mode = gpu.display_mode
                display_active = gpu.display_active
                f_gpu.write(
                    f"{ts},{id},{uuid},{load},{memoryUtil},{memoryTotal},{memoryFree},{driver},{name},{serial},{display_mode},{display_active}\n"
                )
            f_gpu.flush()

            write_sys_metrics(f_sys)

            end_loop = datetime.now().timestamp()
            sleep_time = -1
            
            while sleep_time < 0:
                i += 1
                start_next = start + i
                sleep_time = start_next - end_loop
            time.sleep(sleep_time)


def write_sys_metrics(fout, first=False):
    counters = []

    key_or_val(counters, "timestamp", f"{time.time() * 1000}", first)

    net = psutil.net_io_counters(pernic=True)
    for device in sorted(net):
        net_device = net[device]
        key_or_val(
            counters,
            f"net.bytes_sent.{device}",
            f"{net_device.bytes_sent}",
            first,
        )
        key_or_val(
            counters,
            f"net.bytes_recv.{device}",
            f"{net_device.bytes_recv}",
            first,
        )
        key_or_val(
            counters,
            f"net.packets_sent.{device}",
            f"{net_device.packets_sent}",
            first,
        )
        key_or_val(
            counters,
            f"net.packets_recv.{device}",
            f"{net_device.packets_recv}",
            first,
        )
        key_or_val(counters, f"net.errin.{device}", f"{net_device.errin}", first)
        key_or_val(counters, f"net.errout.{device}", f"{net_device.errout}", first)
        key_or_val(counters, f"net.dropin.{device}", f"{net_device.dropin}", first)
        key_or_val(counters, f"net.dropout.{device}", f"{net_device.dropout}", first)

    disks = psutil.disk_io_counters(perdisk=True)
    for disk in sorted(disks):
        disks_disk = disks[disk]
        key_or_val(
            counters,
            f"disk.read_count.{disk}",
            f"{disks_disk.read_count}",
            first,
        )
        key_or_val(
            counters,
            f"disk.read_bytes.{disk}",
            f"{disks_disk.read_bytes}",
            first,
        )
        key_or_val(
            counters,
            f"disk.write_count.{disk}",
            f"{disks_disk.write_count}",
            first,
        )
        key_or_val(
            counters,
            f"disk.write_bytes.{disk}",
            f"{disks_disk.write_bytes}",
            first,
        )

    cputimes = psutil.cpu_times(percpu=False)
    cpudict = cputimes._asdict()
    for sk in sorted(cpudict):
        sv = cpudict[sk]
        key_or_val(counters, f"cpu.{sk}", f"{sv}", first)

    cpupercent = psutil.cpu_percent()
    key_or_val(counters, f"cpu.percent", f"{cpupercent}", first)

    cpufreq = psutil.cpu_freq()
    key_or_val(counters, f"cpu.freq.current", f"{cpufreq.current}", first)
    key_or_val(counters, f"cpu.freq.min", f"{cpufreq.min}", first)
    key_or_val(counters, f"cpu.freq.max", f"{cpufreq.max}", first)

    cpus = psutil.cpu_stats()
    key_or_val(counters, f"cpu.ctx_switches", f"{cpus.ctx_switches}", first)
    key_or_val(counters, f"cpu.interrupts", f"{cpus.interrupts}", first)
    key_or_val(counters, f"cpu.soft_interrupts", f"{cpus.soft_interrupts}", first)
    key_or_val(counters, f"cpu.syscalls", f"{cpus.syscalls}", first)

    fout.write(f"{','.join(counters)}\n")
    # fout.write(os.linesep)
    fout.flush()


if __name__ == "__main__":
    main()

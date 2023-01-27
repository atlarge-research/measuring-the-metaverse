
# Measuring the Metaverse

This repository contains performance measurement scripts and data for the Meta Quest Pro.

## Quick Links

- [The plots used in our HotCloudPerf article submission](plots/README.md)
- [Experiment overview](experiments/)

## Reproducing Performance Measurements

If you own a Meta Quest Pro, you can use the code in this repository to perform your own performance measurements.
The code might work on other Android-based virtual-reality devices, but we did not test this.
### Setup

This setup assumes a Windows 11 operating system. If you are using another operating system, you will need to rewrite the `run.ps1` script to work on your OS.

Install:

1. Install `adb` and the Meta Quest Pro adb drivers.
2. Python 3.10
   1. Get dependencies: `pip install psutil GPUtil`.

### How to Run

1. Connect the Meta Quest Pro to a gaming PC using a USB-C cable.
2. If you want to do a wireless experiment:
   1. Run `adb tcpip 5555` followed by `adb connect <ip.of.your.headset>:5555` to wirelessly connect to your headset. To find out the IP address of your headset, run `adb shell ip -f inet addr show wlan0`.
   2. Unplug the cable. This is important. The `run.ps1` script relies on there only being one ADB device connected to the gaming PC.
3. Open Wireshark on the gaming PC to start capturing network traffic to the headset.
4. Run `./run.sh` in this repository. This script will perform measurements every second and append them to several `*.log` files. If there is a connection error, the script will try to restart the measurements automatically.
5. ~~Play some games~~ Run the experiment.
6. Hit `ctrl+C` on the `run.sh` script.
7. Stop the network capture in Wireshark.
8. Organize files into a folder belonging to your experiment. 

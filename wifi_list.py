import subprocess
import os
import time
import threading
import queue

# Global flag to control the loop
stop_wifi_search_bool = False

def displayWifi():

    # Function to stop the Wi-Fi search loop
    def stop_wifi_search():
        global stop_wifi_search_bool
        stop_wifi_search_bool = True

    # Function to get the list of available Wi-Fi networks
    def get_wifi_list():
        try:
            res = subprocess.check_output(["nmcli", "-f", "SSID,BSSID,CHAN,SIGNAL,SECURITY", "device", "wifi"], encoding="utf-8")
            return res
        except Exception as e:
            print("Error: ", e)
            return ""

    # Function to continuously display the list of Wi-Fi networks
    def list_as_per_time(q):
        global stop_wifi_search_bool
        while not stop_wifi_search_bool:
            os.system("clear")
            output = get_wifi_list()
            print(output)
            time.sleep(1)
        os.system("clear")
        try:
            q.put(output)
        except:
            pass

    # Function to listen for the Enter key press
    def wait_for_enter():
        input("Press Enter to stop Wi-Fi scanning...\n")
        stop_wifi_search()

    #creating a queue to collect the output from thread
    q = queue.Queue()

    scan_thread = threading.Thread(target=list_as_per_time,args=(q,))
    scan_thread.daemon = True 
    scan_thread.start()
    wait_for_enter()
    scan_thread.join()

    lastOutput = q.get()

    #String manipulation
    def splitAndStore(OutString):
        lines = OutString.strip().split('\n')
        rows = []

        # Parse each line after the header
        for line in lines[1:]:  # Skip the header row
            parts = line.split()  # Split by whitespace
            # SSID may span multiple parts, so find where BSSID starts
            for i, part in enumerate(parts):
                if ":" in part and len(part.split(":")) == 6:  # BSSID detected
                    ssid = " ".join(parts[:i])  # SSID is everything before BSSID
                    bssid = part  # Current part is BSSID
                    chan, signal, security = parts[i + 1], parts[i + 2], " ".join(parts[i + 3:])
                    rows.append([ssid, bssid, chan, signal, security])
                    break
        return rows

    # Print and collect the choice from the user
    def printAndSelect(stringList):
        i = 1
        for wifi in stringList:
            print(f"{i}  :  {wifi}")
            i+=1
        selection = int(input("Select A wifi : "))
        return stringList[selection-1][1],stringList[selection-1][2]


        

    listAsPerLastOut = splitAndStore(lastOutput)
    Bssid,channel = printAndSelect(listAsPerLastOut)
    
    return Bssid,channel



    # def captivePort():
    #     print("Setupping ip forwarding")
    #     subprocess.run(["sudo","sysctl", "-w", "net.ipv4.ip_forward=1"])
    #     print("Updating the iptables or DNS Redirection")
    #     subprocess.run(["sudo","iptables","-t","nat","-A","PREROUTING","-p","tcp","--dport","80","-j","REDIRECT","--to-port","4242"])
    #     with open("/etc/dnsmasq.conf","a") as fi:
    #         fi.write("address=/#/127.0.0.1")
    #     print("restarting systemctl")
    #     subprocess.run(["sudo","systemctl", "restart", "dnsmasq"])
    # captivePort()
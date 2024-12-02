import subprocess

def list_interface():
    # Run the full command in a shell, since we're using pipes and multiple commands
    command = "nmcli device status | grep -e 'wifi' -e 'wl' | awk 'NR==1 {print $1}'"
    
    # subprocess.run to execute the command in the shell
    res = subprocess.run(command, shell=True, capture_output=True, check=True, text=True)
    
    interface=res.stdout.strip()

    return interface

def start_monitor_mode(if_name):
    subprocess.run(["sudo","airmon-ng","start",if_name],text=True,check=True)

def list_monitor_interface():
    cmd="iw dev | grep Interface | awk '{print $2}'"
    inf=subprocess.run(cmd,shell=True,capture_output=True,text=True,check=True)
    mon_if=inf.stdout.strip()
    print(mon_if)
    return mon_if

def stop_monitor_mode(mon_if):
    # cmd="sudo airmon-ng stop"
    subprocess.run(["sudo","ip","link","set",mon_if,"down"])
    subprocess.run(["sudo","iw",mon_if,"set","type","managed"])
    subprocess.run(["sudo","ip","link","set",mon_if,"up"])
    # subprocess.run(["sudo", "airmon-ng", "stop", mon_if], check=True, text=True)

def ls_active_wifi(mon_if):
    ls_Wifi=subprocess.run(["sudo","airodump-ng",mon_if],check=True,text=True)
    print(ls_Wifi)

    
if __name__ == "__main__":
    ifname=list_interface()
    mon_if=list_monitor_interface()
    choice=input("""1.List Interface
                    2.Start Monitor
                    3.Stop Monitor
                    4.List Wifi Networks
                    """)
    if choice=="1":
        list_interface()
    if choice=="2":
        start_monitor_mode(ifname)
    if choice=="3":
        stop_monitor_mode(mon_if)
    if choice=="4":
        ls_active_wifi(mon_if)



import sys, os.path, subprocess, paramiko, time, re,threading,datetime


# Checking the IP file Validity
def ipValidate():
    file = input("\n# Enter the full IP file path: ")

    if os.path.isfile(file) == True:
        print("\n* Valid IP file.\n")

    else:
        print(f"\n* Invalid file path {file} Please recheck and try agin.\n")
        sys.exit()

    ip_select = open(file,"r")
    ip_select.seek(0)
    list0 = ip_select.readlines()
    ip_select.close()

    return list0 

# Checking the IP Addresses Validity

def checkAdder(ips):
    for ip in ips:
        ip = ip.rstrip("\n")
        octet = ip.split(".")

        if (len(octet)==4) and (1<= int(octet[0]) <= 223) and (int(octet[0]) != 127) and (int(octet[0]) != 169 or int(octet[1]) != 254) and (0 <= int(octet[1]) <= 255 and 0<= int(octet[2]) <=255 and 0<= int(octet[3]) <=255):
            continue

        else:
            print(f"\n* The file containe an Invalid IP address: {ip} ")
            sys.exit()

# Checking the reachability of theIP Addresses

def reach(ips):

    for ip in ips:
        ip = ip.rstrip("\n")
        ping = subprocess.call(f'ping {ip} -c 2', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# replace the -c with an -n in windows

        if ping == 0:
            print(f"\n* {ip} is reachable")
            continue
        else:
            print(f"\n* {ip} is not reachable. Check your connection")
            sys.exit()

# Establishing the SSH connections

uFile = input("\n# Enter the full Authantication file path: ")

if os.path.isfile(uFile) == True:
    print("\n Authantication file is Valid. \n")

else:
    print(f"\n file {uFile} does not exist")
    sys.exit()


def ssh(ip):
    global uFile
    global cmd

    try:
        selectFile = open(uFile,"r")
        selectFile.seek(0)

        username = selectFile.readlines()[0].split(",")[0].rstrip("\n")
        selectFile.seek(0)
        secret = selectFile.readlines()[0].split(",")[1].rstrip("\n")

        start = paramiko.SSHClient()

        start.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        start.connect(ip.rstrip("\n"), username=username, password=secret)

        connect = start.invoke_shell()

        connect.send("enable\n")
        connect.send("terminal length 0\n")
        connect.send("show processes top once\n")#the command to show the cpu performence


        time.sleep(3)
        routePut = connect.recv(65535)

        if re.search(b"% Invalid input", routePut):
            print(f"* IOS syntax error on device {ip} ")

        else:
            print(f"\nDone for {ip} Send at {str(datetime.datetime.now())}")
        try:
            cp = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)* us,", routePut)

            utilize = cp.group(2).decode("utf-8")

            with open("./cpu.txt","a") as file:
                file.write(utilize + "\n")
            start.close()
        except:
            pass
    except paramiko.AuthenticationException:
        print("Invalid username or password. Check the authantication file")
        print("Closeing ...")

def thread(list1, f):
    
    thr = []

    for i in list1:
        t = threading.Thread(target= f, args=(i,))
        t.start()
        thr.append(t)

    for t in thr:
        t.join()
    

ips = ipValidate()

try:
    va = True
    checkAdder(ips)

except KeyboardInterrupt:
    print("\nExiting the program....\n")
    sys.exit()
def startG():
    try:
        gr = "./graph.py"
        if os.path.isfile(gr) == True:
            print("\n*Starting the graph...")
            subprocess.call(f"python3 {gr}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            global va
            va = False
        else:
            print("File does not exist.")
    except KeyboardInterrupt:
        print("Exiting...")
try:
    reach(ips)
except KeyboardInterrupt:
    print("\nExiting....\n")
    sys.exit()

    
def callD():
    while True:
        try:
            if va == True:
                thread(ips,ssh)
            else:
                print("\nExiting...")
                break
        except KeyboardInterrupt:
            print("\n Exiting Program....")
            break

try:
    threading.Thread(target=startG).start()
    threading.Thread(target=callD).start()
except KeyboardInterrupt:
    print("Exiting....")
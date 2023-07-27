import random
import requests
import traceback
import time
import threading
import signal
import sys

# url = "https://phonenumbervalidatefree.p.rapidapi.com/ts_PhoneNumberValidateTest.jsp"
# url = 'https://phonenumbervalidatefree.p.rapidapi.com/ts_PhoneNumberValidateTest.jsp'
# url ='https://veriphone.p.rapidapi.com/verify'
# url = 'https://bulk-whatsapp-validator.p.rapidapi.com/free/wchk'
url = 'https://validate-phone-by-api-ninjas.p.rapidapi.com/v1/validatephone'
headers = {'X-RapidAPI-Key': 'fde1c0b871msh52cb92583a98140p1ec184jsn31ae967f9fc7',
    'X-RapidAPI-Host': 'validate-phone-by-api-ninjas.p.rapidapi.com'}

output = []
results = []
raw = []
dat = []
info = []

checked = 0
threadNum = 100


location = input("File Location: ")
amountToGenerate = int(input("Amount to Generate: "))




def worker(index):
    global checked
    global output
    global results
    global raw
    global url
    global headers
    global phoneNumLength
    global amountToGenerate
    global threadNum
    global dat
    global info
    
    # time.sleep(1)
    pos = random.randint(0, len(info))
    chosen = info[pos].split("\n")[0][0:7]
    # print(pos, chosen, (len( info[pos]) - len(chosen)) ** 10, len(info[pos]), len(chosen), info[pos])
    for i in range(amountToGenerate // threadNum):
       
        ending = []
        for i in range(len(info[pos]) - len(chosen) - 1):
            ending.append(str(random.randint(0, 9)))
        
        

        # print(temp)


        response = requests.get(url, headers=headers, params={"number": chosen + "".join(ending)})
        # print(temp)
        # print(response.json())
        if(response.status_code == 200):
            dat.append(response.json())
            data = response.json()
            # print(data)
            if(data["is_valid"] == True and data["country"] == "United Kingdom"):
                # print(True)
                results.append(chosen + "".join(ending) + "\n")
                raw.append(data)
        checked+=1
        # print(checked)
        print(str(checked) + "/" + str(amountToGenerate), end="\r")
try:
    try:

        
        print("Running...")
        with open(location + ".txt", "r") as inp:
            content = inp.readlines()

            for line in content:
                if line not in info:
                    info.append(line)
            # print(info)
            # print(len(info))
            # print(content)
            threads = []
            for i in range(threadNum):
                t = threading.Thread(target=worker, args={i})
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

            # print(dat)
            print(len(raw))

            for num in raw:
                # print(num)
                if "/" in num["location"]:
                    num["location"] = num["location"].split("/")[0]
                with open("eng/" + num["location"] + ".txt", "a") as out:
                    out.write(num["format_e164"] + "\n")


            with open(location + ".txt", "a") as out:
                out.writelines(results)
                print("Finished")


    except Exception as e:
        print(str(e))
        traceback.print_exc()
        for num in raw:
                # print(num)
                try:
                    if "/" in num["location"]:
                        num["location"] = num["location"].split("/")[0]
                    with open("eng/"+num["location"] + ".txt", "a") as out:
                         out.write(num["format_e164"] + "\n")
                except Exception as ex:
                    print(str(ex))

        with open(location + ".txt", "a") as out:
            out.writelines(results)
            print("Finished")
        print("An error occured")


except KeyboardInterrupt:
    print(raw)
    print(results)
    for num in raw:
                # print(num)
        try:
            with open(num["location"] + ".txt", "a") as out:
                 out.write(num["format_e164"] + "\n")
        except Exception as ex:
            print(str(ex))

    with open("output.txt", "a") as out:
        out.writelines(results)
        print("Finished")
    print("An error occured")

def signal_handler(signal, frame):
    print('Keyboard interrupt detected. Exiting...')
    for num in raw:
                # print(num)
        try:
            with open(num["location"] + ".txt", "a") as out:
                 out.write(num["format_e164"] + "\n")
        except Exception as ex:
            print(str(ex))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

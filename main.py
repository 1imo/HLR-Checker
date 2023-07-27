import random
import requests
import traceback
import time
import threading

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

checked = 0
threadNum = 100


phoneNumLength = int(input("Length of phone number: "))
amountToGenerate = int(input("Amount to generate: "))

def worker():
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
    for x in range(int(amountToGenerate / threadNum)):
        # time.sleep(1)
        chosen = content[random.randint(0, len(content) - 1)]
        prefix = chosen.split("\n")[0]
            
        ending = []
        for i in range(phoneNumLength - len(prefix)):
            ending.append(str(random.randint(0, 9)))
        # print(prefix + "".join(ending))
        response = requests.get(url, headers=headers, params={"number": "+" + prefix + "".join(ending)})
        # print(response)
        dat.append(response.json())
        if(response.status_code == 200):
            data = response.json()
            # print(data)
            if(data["is_valid"] == True and data["country"] == "United Kingdom"):
                # print(True)
                results.append("+" + str(prefix) + "".join(ending) + "\n")
                raw.append(data)
        checked+=1
        print(str(checked) + "/" + str(amountToGenerate), end="\r")
try:
    try:

        
        print("Running...")
        with open("eng/inputEng.txt", "r") as file:
            content = file.readlines()
            # print(content)
            threads = []

            for i in range(threadNum):
                t = threading.Thread(target=worker)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            # print(dat)

            for num in raw:
                # print(num)
                if "/" in num["location"]:
                    num["location"] = num["location"].split("/")[0]
                with open("eng/" + num["location"] + ".txt", "a") as out:
                    out.write(num["format_e164"] + "\n")


            with open("eng/output.txt", "a") as out:
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

        with open("eng/output.txt", "a") as out:
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

import random
import requests
import traceback
import time
import threading

# url = "https://phonenumbervalidatefree.p.rapidapi.com/ts_PhoneNumberValidateTest.jsp"
# url = 'https://phonenumbervalidatefree.p.rapidapi.com/ts_PhoneNumberValidateTest.jsp'
# url ='https://veriphone.p.rapidapi.com/verify'
# url = 'https://bulk-whatsapp-validator.p.rapidapi.com/free/wchk'
# url = 'https://validate-phone-by-api-ninjas.p.rapidapi.com/v1/validatephone'
url = 'https://phone-number-validation-api.p.rapidapi.com/checkNumber'
headers = {'content-type': 'application/x-www-form-urlencoded',
    'X-RapidAPI-Key': '58b5a6d3d5mshdc43a1089ddec90p1a5766jsn7a8bcf99ac0d',
    'X-RapidAPI-Host': 'phone-number-validation-api.p.rapidapi.com'}

output = []
results = []
raw = []
dat = []
content = []

checked = 0
threadNum = 100


# phoneNumLength = int(input("Length of phone number: "))
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
    global content
    for x in range(len(content) // threadNum):
        # time.sleep(1)
        # print(content[1], content[2])
        chosen = content[random.randint(0, len(content))][1:]
        # print(content[x])
        # print(chosen.split())
        prefix = chosen.split("\n")[0]
        if(amountToGenerate == x):
            break
            
        # print(chosen)
        # response = requests.post(url, headers=headers, data=chosen)
        url = "https://phone-number-validation-api.p.rapidapi.com/checkNumber"
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
    'X-RapidAPI-Key': '58b5a6d3d5mshdc43a1089ddec90p1a5766jsn7a8bcf99ac0d',
    'X-RapidAPI-Host': 'phone-number-validation-api.p.rapidapi.com'
        }
        data = {
            "phone": chosen,
            "country-code": "GB"
        }

        response = requests.post(url, headers=headers, data=data)
        # time.sleep(0.1)
            # print(data)
        if(response.status_code == 200):
            dat.append(response.json())
            data = response.json()
            # print(response.json())
            try:
                if(data["valid"] == True and data["location"] == "United Kingdom"):
                    # print(True)
                    # print(data)
                    # print()
                    # results.append("+" + str(prefix) + "".join(ending) + "\n")
                    raw.append(data)
            except Exception as err:
                print(str(err))
        checked+=1
        print(str(checked) + "/" + str(amountToGenerate), end="\r")
try:
    try:

        
        print("Running...")
        with open("eng/output.txt", "r") as file:
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
                try:
                
                    with open("eng/" + num["network"] + ".txt", "a") as out:
                        out.write(num["international-number"] + "\n")
                except Exception as err:
                    print(str(err))


            # with open("eng/output.txt", "a") as out:
            #     out.writelines(results)
            #     print("Finished")


    except Exception as e:
        print(str(e))
        traceback.print_exc()
        for num in raw:
                # print(num)
                try:
                    
                    with open("eng/"+num["network"] + ".txt", "a") as out:
                         out.write(num["international-number"] + "\n")
                except Exception as ex:
                    print(str(ex))

        # with open("eng/output.txt", "a") as out:
        #     out.writelines(results)
        #     print("Finished")
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

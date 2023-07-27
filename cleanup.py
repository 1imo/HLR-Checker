import os

dup = 0

for item in os.listdir("eng/"):
    print(item)
    if ".txt" in item:
        used = []
        try:
            with open("eng/" + item, 'r') as file:
                content = file.readlines()
                for num in content:
                    if num.split("\n")[0] not in used:
                        used.append(num)
                    else:
                        dup+=1
                        print("Duplicate No" + dup, end="\r")
                with open("eng/" + item, 'w') as out:
                    out.writelines(used)
        except Exception as e:
            print(str(e))



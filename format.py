with open("canada/Quebec.txt") as input:
    content = input.readlines()
    print(content)

    num = 0

    for number in content:
        num+=1
        if(num >= 3499):
            break
        with open("formatted.txt", "a") as output:
            number = number.replace("+", "")
            output.write(number)
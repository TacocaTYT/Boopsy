while True:
    try:
        user_input = "0+" + input("Equation: ").replace("^","**").replace("x","*").replace("X","*")
        if any(c.isalpha() or c.isspace() for c in user_input):print("Not a valid equation")
        else:y = "print(" + user_input + ")";exec(y)
    except:print("ERROR - Stop breaking stuff")
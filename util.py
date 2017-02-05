def flatten(l):
    return [item for sublist in l for item in sublist]

def print_error(s):
    print("\n\033[1;31mError: " + s + "\033[0;37m\n")

def normalize(s):
    name = s
    for unnecessary_char in "- ":
        name = name.replace(unnecessary_char,"")
    return name.lower()

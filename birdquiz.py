import yaml
from random import shuffle

def flatten(l):
    return [item for sublist in l for item in sublist]

def print_error(s):
    print("\n\033[1;31mError: " + s + "\033[0;37m\n")

def normalize(s):
    name = s
    for unnecessary_char in "- ":
        name = name.replace(unnecessary_char,"")
    return name.lower()

def study(quiz_set):
    #it's not actually shuffled yet. I dislike in-place functions.
    shuffled_birdlist = quiz_set
    shuffle(shuffled_birdlist)
    for bird in shuffled_birdlist:
        print(bird)

def quiz_loop(birds):
    choice = ""
    while choice != "q":
        print("Choose a category to study:\n")
        categories = list(birds.keys())
        for i,category in enumerate(categories):
            print("[" + str(i) + "] " + category)
        print("[*] All categories")
        print("[q] Exit")

        choice = input("Your choice: ")

        quiz_set = []

        if choice == "*":
            quiz_set = flatten([birds[x] for x in categories])
        elif choice == "q":
            return
        else:
            try:
                index = int(choice)
                quiz_set = birds[categories[index]]
            except:
                print_error("Invalid choice.")
                continue

        study(quiz_set)

def main():
    birds = {}
    with open("birdlist.yaml", 'r') as f:
        birds = yaml.load(f)

    quiz_loop(birds)

main()

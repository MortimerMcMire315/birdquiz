import yaml
import dryscrape
import signal
from util import flatten, print_error, normalize
from mp3grab import play_mp3_from_birdname, play_mp3
from random import shuffle

def stop_mp3(mp3_process):
    mp3_process.send_signal(signal.SIGINT)
    mp3_process.wait()

def study(quiz_set, webkit_session):
    #it's not actually shuffled yet. I dislike in-place functions.
    shuffled_birdlist = quiz_set
    correct = []
    while shuffled_birdlist:
        print("--------------------")
        shuffle(shuffled_birdlist)
        birdname = shuffled_birdlist[0]

        mp3_result = play_mp3_from_birdname(birdname,webkit_session)
        if mp3_result is None:
            print("mp3 could not be found. Taking \"" + birdname + "\" out of this rotation. Sorry...")
            correct.append(birdname)
            continue
        (mp3_process, mp3_path) = mp3_result

        mp3loop = True
        while True:
            print("[a] Enter an answer")
            print("[r] Restart the bird call")
            print("[?] Give up and get the answer")
            print("[q] Quit and go back to the category menu")
            what_next = input("> ")

            if what_next in ['r','q']:
                stop_mp3(mp3_process)

            if what_next == 'a':
                answer = input("Your answer: ")
                if normalize(answer) == normalize(birdname):
                    print("Correct!")
                    stop_mp3(mp3_process)
                    correct.append(birdname)
                    break
                else:
                    print("Incorrect.")

            elif what_next == 'r':
                (mp3_process,mp3_path) = play_mp3(mp3_path)

            elif what_next == '?':
                print("Answer: " + birdname)
                mp3loop = False
                giveuploop = True
                while True:
                    print("\n[a] Add this bird back into the rotation")
                    print("[i] Ignore it and continue")
                    print("[r] Restart the bird call")
                    giveupchoice = input("> ")
                    if giveupchoice == 'r':
                        stop_mp3(mp3_process)
                        (mp3_process,mp3_path) = play_mp3(mp3_path)
                    elif giveupchoice == 'i':
                        correct.append(birdname)
                        stop_mp3(mp3_process)
                        break
                    elif giveupchoice == 'a':
                        stop_mp3(mp3_process)
                        break
                    else:
                        print_error("Invalid choice.")
                break

            elif what_next == 'q':
                return
            else:
                print_error("Invalid choice.")

        shuffled_birdlist = list(set(shuffled_birdlist).difference(set(correct)))

    print("Category finished.")
    print("==================")


def quiz_loop(birds, webkit_session):
    choice = ""
    while choice != "q":
        print("Choose a category to study:\n")
        categories = list(birds.keys())
        for i,category in enumerate(categories):
            print("[" + str(i) + "] " + category)
        print("[*] All categories")
        print("[q] Exit")

        choice = input("> ")

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

        study(quiz_set, webkit_session)

def main():
    webkit_session = dryscrape.Session()
    birds = {}
    with open("birdlist.yaml", 'r') as f:
        birds = yaml.load(f)

    quiz_loop(birds, webkit_session)

main()

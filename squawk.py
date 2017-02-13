import yaml
import signal
from util import flatten, print_error, normalize, set_difference
from mp3grab import play_mp3_from_birdname, play_mp3
from random import shuffle

def stop_mp3(mp3_process):
    mp3_process.send_signal(signal.SIGINT)
    mp3_process.wait()

def quiz_loop(birds):
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

        study(quiz_set)

'''
Quiz the user on the given list of bird names
'''
def study(quiz_set):
    birdlist = quiz_set
    skiplist = []
    while birdlist:
        print("--------------------")
        shuffle(birdlist)
        birdname = birdlist[0]

        mp3_result = play_mp3_from_birdname(birdname)
        if mp3_result is None:
            print("mp3 could not be found. Taking \"" + birdname + "\" out of this rotation. Sorry...")
            skiplist.append(birdname)
            birdlist = set_difference(list1, list2)
            continue

        (mp3_process, mp3_path) = mp3_result

        (skiplist, keep_quizzing) = ask_user_about_bird(birdname, skiplist, mp3_process, mp3_path)
        if keep_quizzing is False:
            return

        birdlist = list(set(birdlist).difference(set(skiplist)))

    print("Category finished.")
    print("==================")

'''
Given a bird name, a list of skipped bird names, and an MP3 of the selected
bird's call, Quiz the user on the selected bird.

Returns: (List, Bool) - the updated list of skipped bird names and a boolean
that is True if the user would like to continue being quizzed, and False
otherwise.
'''
def ask_user_about_bird(birdname, skiplist, mp3_process, mp3_path):
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
                skiplist.append(birdname)
                return(skiplist, True)
            else:
                print("Incorrect.")

        elif what_next == 'r':
            (mp3_process,mp3_path) = play_mp3(mp3_path)

        elif what_next == '?':
            return(user_giveup(birdname, skiplist, mp3_process, mp3_path), True)
        elif what_next == 'q':
            return(skiplist, False)
        else:
            print_error("Invalid choice.")

'''
Called when the user has chosen to give up and get an answer.  Gives options to
add the bird back into the rotation, ignore it (a.k.a. add it to the skiplist),
or repeat the call.  Returns the updated list of birds to skip.
'''
def user_giveup(birdname, skiplist, mp3_process, mp3_path):
    print("Answer: " + birdname)
    while True:
        print("\n[a] Add this bird back into the rotation")
        print("[i] Ignore it and continue")
        print("[r] Restart the bird call")
        giveupchoice = input("> ")
        if giveupchoice == 'r':
            stop_mp3(mp3_process)
            (mp3_process,mp3_path) = play_mp3(mp3_path)
        elif giveupchoice == 'i':
            skiplist.append(birdname)
            stop_mp3(mp3_process)
            return(skiplist)
        elif giveupchoice == 'a':
            stop_mp3(mp3_process)
            return(skiplist)
        else:
            print_error("Invalid choice.")
    return(skiplist)

def main():
    birds = {}
    with open("birdlist.yaml", 'r') as f:
        birds = yaml.load(f)

    quiz_loop(birds)

main()

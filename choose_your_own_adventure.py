print("========================================")
print("   WELCOME TO THE WHISPERING WOODS")
print("========================================")
name = input("Type your name: ").strip()
print(f"\nWelcome, {name}! The forest is watching you...\n")

while True:
    answer = input("You stand at a fork in the forest. Do you go left, right, or stay still? (type 'left', 'right', or 'stay')\n: ").strip().lower()

    if answer == "quit":
        print("Thanks for playing, brave adventurer!")
        break

    if answer == "left":
        print("\nYou follow a narrow trail deeper into the woods.")
        answer = input("You hear a roar and spot a wild bear blocking the path. Do you run, hide, or fight? (type 'run', 'hide', or 'fight')\n: ").strip().lower()

        if answer == "run":
            print("You sprint through the bushes and discover a hidden cabin. Inside, you find food and a map. You escape the forest and become a legend!")
        elif answer == "hide":
            print("You hide behind a giant tree. The bear sniffs the air, then wanders off. You survive, but the forest still feels haunted.")
        elif answer == "fight":
            print("You charge at the bear with courage, but it is far stronger. The forest goes silent as your adventure ends here.")
        elif answer == "quit":
            print("Thanks for playing, brave adventurer!")
            break
        else:
            print("Invalid choice. Please try again.")

    elif answer == "right":
        print("\nYou walk toward a glowing clearing.")
        answer = input("In the middle of the clearing sits a treasure chest. Do you open it, inspect it, or leave it? (type 'open', 'inspect', or 'leave')\n: ").strip().lower()

        if answer == "open":
            print("You open the chest and discover a golden key, a map, and a strange crystal. The forest trembles and reveals a secret path out. You win!")
        elif answer == "inspect":
            print("You carefully study the chest and notice old carvings of stars. When you touch the carvings, the chest unlocks itself and reveals a magical amulet. You are now protected by the forest.")
        elif answer == "leave":
            print("You leave the chest behind and continue deeper into the forest. The path twists into darkness, and you are lost forever.")
        elif answer == "quit":
            print("Thanks for playing, brave adventurer!")
            break
        else:
            print("Invalid choice. Please try again.")

    elif answer == "stay":
        print("\nYou stand perfectly still and listen to the forest breathe. A whisper says: 'Only the brave may pass.'")
        answer = input("Do you follow the whisper, ignore it, or call out? (type 'follow', 'ignore', or 'call')\n: ").strip().lower()

        if answer == "follow":
            print("The whisper leads you to a moonlit waterfall, where you find a glowing sword and a hidden path home. You leave the woods stronger than before.")
        elif answer == "ignore":
            print("You ignore the whisper, but the forest grows restless. A shadow swallows the trail behind you, and your adventure ends in the mist.")
        elif answer == "call":
            print("You speak into the darkness, and a wise old fox steps out of the trees. It grants you a single wish and sends you safely home.")
        elif answer == "quit":
            print("Thanks for playing, brave adventurer!")
            break
        else:
            print("Invalid choice. Please try again.")

    else:
        print("Invalid choice. Please type 'left', 'right', 'stay', or 'quit'.")

    play_again = input("\nDo you want to play again? (type 'yes' or 'no')\n: ").strip().lower()
    if play_again != "yes":
        print("\nThanks for playing, " + name + "! Until next time...")
        break

print("\n=== END OF ADVENTURE ===")
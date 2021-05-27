password = input("Put password")
answer = '_' * len(password)
lives = 3

while(lives>0 and answer != password):
    print(answer)
    print("Number of lives: " + str(lives))
    guess = input("Guess 1 letter")
    while(len(guess) != 1):
        print("Wrong input!")
        guess = input("Guess 1 letter!")
    index = 0
    damage = True
    for character in password:
        if(character == guess):
            answer = answer[:index] + character + answer[index + 1:]
            damage = False
        index = index + 1
    if(damage):
        lives = lives - 1

if(lives == 0 ):
    print("You lost!")
else:
    print("You won!")

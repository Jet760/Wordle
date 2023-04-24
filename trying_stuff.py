guess = "habga"
target = "hhbba"
#score = [0, 0, 0, 0, 0]

for i, char in enumerate(guess):
    if char in target:
        if guess[i] == target[i]:
            score[i] = 2
        else:
            score[i] = 1
    else:
        pass




print(score[0])
print(score[1])
print(score[2])
print(score[3])
print(score[4])

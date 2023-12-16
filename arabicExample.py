from random import randint

g = int(input("What is your first guess? "))
guesses = [g]
acc = randint(1, 100)

while g is not acc:
	if g < acc: g = int(input("too low! "))
	elif g > acc: g = int(input("too high! "))
	guesses.append(g)

print(f"\nYou got it! The value was {acc}. Your guesses were {guesses} with a number of {len(guesses)}\n")
guesses.sort()
guesses.reverse()
print(f"Your sorted guesses are {guesses}")
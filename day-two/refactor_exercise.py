# This code will counts letters and prints a graph

x = "The modern digital computer was invented and intended as a device that should facilitate and speed up complicated and time-consuming computations. In the majority of applications its capability to store and access large amounts of information plays the dominant part and is considered to be its primary characteristic, and its ability to compute, i.e., to calculate, to perform arithmetic, has in many cases become almost irrelevant. In all these cases, the large amount of information that is to be processedin some sense represents an abstraction of a part of the real world. The  information that is available to the computer consists of a selected set of data about the real world, namely, that set which is considered relevant to the problem at hand, that set from which it is believed that the desired results can be derived. The data represent an abstraction of reality in the sense that certain properties and characteristics of the real objects are ignored because they are peripheral and irrelevant to the particular problem. An abstraction is thereby also a simplification of facts."

a = {}
a = dict(zip("abcdefghijklmnopqrstuvwxyz", [0]*26))

# Count the letters in the string
for i in "abcdefghijklmnopqrstuvwxyz":
    for j in x.lower():
        if i == j:
            a[j] = a[j] + 1

# Sum them
t = 0
for k in a:
    t = t + a[k]

# Get the frequencies
b = dict(zip("abcdefghijklmnopqrstuvwxyz",[0]*26))
for k in a:
    b[k] = a[k]/t

# Print histogram
t = 50
for k in b:
    print(k + " : " + "#"*int(t*b[k]))

# describe rarity:
c = ""
uc = ""
r = ""
for k in b:
    if b[k] > 0.1:
        c += k
    elif b[k] > 0.05:
        uc += k
    else:
        r += k
print("Common: " + c)
print("Uncommon: " + uc)
print("Rare: " + r)
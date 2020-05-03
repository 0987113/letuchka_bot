a = ['1', 2, '3', 4, 5, 6, 7, 8, 9]

"""for b in range(len(a)):
    print(b)"""

"""num = [i for i in range(len(a))]
print(num)"""

"""for i in range(len(a)[0::3]):
    print(i)"""
print(str(len(a)), type(str(len(a))))
print(range(len(a))[0::3])
print(a[0::3])

num_buttons = [i for i in range(len(a) + 1)[0::3]]
print(num_buttons)




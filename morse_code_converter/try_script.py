#!bin/user/python3
a_dict = {1:'a',
          2: 'b',
          3: 'c',}

reversed_dict = {value: key for key, value in a_dict.items()}
print(a_dict)
print(reversed_dict)


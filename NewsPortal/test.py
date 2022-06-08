sensored = ['Редиска','редиска','Редиску','редиску','Редиски', 'редиски']
value = 'Охренеть какая редиска выросла в огороде'
x = value.split()
print(x)
for i in range(0, len(x)):
    if x[i] in sensored:
        x[i] = x[i][0] + "***"
value = ' '.join(x)
print(value)

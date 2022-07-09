lst_in = ['1 2 3 4',
          '5 6 7 8',
          '9 8 7 6']

lst2D = list((list(map(int, i.split(' '))) for i in lst_in))

lst2D_int = list(list(int(i) for i in lst ) for lst in lst2D)
print(lst2D_int)

for i in zip(*lst2D_int):
    print(*i, sep=' ')

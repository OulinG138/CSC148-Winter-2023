lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14]]

for sublst in list(map(list, zip(*lst[:-1]))):
    if lst[-1] != []:
        sublst.append(lst[-1].pop(0))
    print(sublst)

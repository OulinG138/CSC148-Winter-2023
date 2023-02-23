from grouper import slice_list

def f(lst):
    output = []

    for sublst in list(map(list, zip(*lst[:-1]))):
        if lst[-1] != []:
            sublst.append(lst[-1].pop(0))
        output.append(sublst)

    return output

if __name__ == '__main__':
    lst = slice_list([1, 2, 3, 4], 2)
    print(f(lst))
def moves_to_nested_dict(moves):
    while [] in moves:
        moves.remove([])
    if len(moves) == 0:
        return {}

    # moves.sort(key=lambda x: x[0])
    tmp = {}
    for game in moves:
        if game[0] not in tmp:
            tmp[game[0]] = []
        tmp[game[0]].append(game[1:])
    res = {}
    for k, v in tmp.items():
        count = v.count([])
        res[(k, count)] = moves_to_nested_dict(tmp[k])
        
    return res


# lst = [["a", "b", "c", 'e'], ['a', 'b']]
# result = make_dict(lst)
# print(result)





# Merge dictionaries with same first two keys
# merged_result = {}
# for k1, v1 in result.items():
#     if k1[:2] not in merged_result:
#         merged_result[k1[:2]] = v1
#     else:
#         merged_result[k1[:2]] = {**merged_result[k1[:2]], **v1}

# print(merged_result)



# nested_list = [["a", "b", "c"], ["a", "b"], ["d", "e"], ["d", "e"]]
# print(list_to_dict(nested_list))






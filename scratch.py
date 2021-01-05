


list_1 = [1,2,3,4,5,6,7,8,9,10]
list_2 = [1,2,3,8,9,10,11,12]

temp = []

cnt = 0
while(1):

    el_1 = list_1[cnt]
    el_2 = list_2[cnt]

    if el_1 not in temp:
        if el_1 == el_2:
            temp.append(el_1)
        else:
            temp.append(el_1)
            list_2.insert(cnt, el_1)
            if el_2 not in list_1:
                temp.append(el_2)

    cnt += 1

def getServer(server_num, input_list, result):
    list_length = len(input_list)
    least_num = min(i for i in input_list if i > 0)
    index_num = input_list.index(least_num)
    result = result + least_num

    if index_num >= 1 and index_num <= (list_length-2):
        input_list[index_num] = -1
        if input_list[index_num -1] > input_list[index_num + 1]:
            input_list[index_num -1] = -1
        elif input_list[index_num -1] < input_list[index_num + 1]:
            input_list[index_num + 1] = -1
        elif input_list[index_num -1] == input_list[index_num + 1]:
            if index_num -1 == 0 and index_num + 1 == list_length:
                input_list[index_num -1] = -1 
            elif index_num -1 == 0 and index_num + 1 != list_length:
                input_list[index_num -1] = -1
            elif index_num -1 != 0 and index_num + 1 == list_length:
                input_list[index_num + 1] = -1
        
    if index_num == 0:
        input_list[index_num + 1] = -1
    
    if index_num == list_length -1:
        input_list[index_num -1] = -1

    server_num = server_num -2

    if server_num > 0:
        getServer(server_num, input_list, result)
    else:
        print(result)

test_list = [1000, 560, 30, 85, 100]
result = 0
getServer(3,test_list, result)
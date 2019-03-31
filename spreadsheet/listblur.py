def blur_list(input_list, kernal_size):
    """Averages list in 1D based on kernal_size"""
    edge = kernal_size // 2
    for i in range(-edge, edge+1):
        print(i)
    temp_list = [0.0] * len(input_list)
    for index in range(len(input_list)):
        item_count = 0
        for adjacent in range( -edge, edge+1 ):
            if ( 0 <= (index + adjacent) <= (len(input_list)-1) ):
                temp_list[index] += input_list[index + adjacent]
                item_count += 1
        temp_list[index] /= float(item_count)
    return temp_list

test = [1,2,3,4,5,6,3,2,1]
print(blur_list(test, 3))

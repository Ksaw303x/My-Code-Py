
num_tot = 0
for num in range(1000, 10000):
    str_num = str(num)

    # if str_num[0] == str_num[3] and str_num[1] == str_num[2] and str_num[1] != '0':
    #if str_num[0] != str_num[3] and str_num[1] != str_num[2] and str_num[2] == '0':
    if str_num[2] == '0':
        num_tot += 1

print(num_tot)
    
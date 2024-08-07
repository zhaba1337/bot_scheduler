import calendar


#print(*calendar.Calendar(0).monthdays2calendar(2014, 6))
matrix_days = [['-']*7]*5
#print(matrix_days)
obj = calendar.Calendar(0).monthdays2calendar(2017, 6)

for i in range(len(obj)):
    #print(obj[i])
    print(i)
    for j in range(len(obj)):
        matrix_days[i][j] =obj[i][j][0]
    print(matrix_days)
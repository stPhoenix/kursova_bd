from random import randint, random
import datetime

query = 'INSERT INTO F_Entity(F_Entity_Price, F_Entity_Quantity, F_Entity_Height, F_Entity_Width, F_Entity_Length, F_Entity_Color, F_Type_ID, F_Maker_ID, F_Material_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s); \n'
maker = [1, 2, 3]
material = [1, 2 ,3]
f_type = [1, 2, 3, 4]
color = ['"White"', '"Green"', '"Yellow"', '"Red"']
quantity = 50

with open('queries/entity.sql', 'w') as f:
    for i in range(quantity):
        q = query % (randint(0, 300), randint(0, 30), randint(0, 100), randint(0, 200), randint(0, 50), color[randint(0, 3)], f_type[randint(0, 2)], maker[randint(0, 2)], material[randint(0, 2)])
        f.write(q)


def randomtimes(start, end):
    frmt = '%Y-%m-%d'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    td = etime - stime
    ntime = random() * td + stime
    return "\""+ntime.strftime(frmt)+"\""

query_sale = 'INSERT INTO F_Sales(F_Entity_ID, F_Sales_Quantity, F_Entity_Date) VALUES (%s, %s, %s);\n'

with open('queries/sales.sql', 'w') as f:
    for i in range(50):
        q = query_sale % (randint(0, quantity), randint(0, 100), randomtimes('2016-01-01', '2020-01-01'))
        f.write(q)


print('Finished')
from random import randint

query = 'INSERT INTO F_Entity(F_Entity_Price, F_Entity_Quantity, F_Entity_Height, F_Entity_Width, F_Entity_Length, F_Entity_Color, F_Type_ID, F_Maker_ID, F_Material_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s); \n'
maker = [1, 2, 3]
material = [1, 2 ,3]
f_type = [4, 5, 6, 7]
color = ['"White"', '"Green"', '"Yellow"', '"Red"']

with open('entity.sql', 'w') as f:
    for i in range(50):
        q = query % (randint(0, 300), randint(0, 30), randint(0, 100), randint(0, 200), randint(0, 50), color[randint(0, 3)], f_type[randint(0, 2)], maker[randint(0, 2)], material[randint(0, 2)])
        f.write(q)

print('Finished')
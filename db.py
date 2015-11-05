import mysql.connector
import sys
from PIL import Image
import base64
import cStringIO
import PIL.Image

db = mysql.connector.connect(user='root', password='test123',
                              host='192.168.3.47',
                              database='eschaton')

#image = Image.open('C:\Users\Abhi\Desktop\cbir-p\images.jpg')
with open("C:\Users\Public\Pictures\Sample Pictures\lachelndes-gesicht_318-85957.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

#blob_value = open('C:\Users\Abhi\Desktop\cbir-p\images.jpg', 'rb').read()
sql = 'INSERT INTO img(images) VALUES(%s)'    
args = (encoded_string, )
cursor=db.cursor()
cursor.execute(sql,args)
sql1='select * from img'
cursor.execute(sql1)
data=cursor.fetchall()
#print type(data[0][0])
data1=base64.b64decode(data[0][0])
file_like=cStringIO.StringIO(data1)
img=PIL.Image.open(file_like)
img.show()

db.close()
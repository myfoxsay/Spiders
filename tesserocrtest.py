import tesserocr
from PIL import Image
image=Image.open('images/DKDSU7362E74VOOAQ7NSQ2Q.png')
print(tesserocr.image_to_text(image,lang='chi_sim'))
print(tesserocr.file_to_text('images/test.jpg'))


#灰度与二值化处理
image=Image.open('images/CheckCode.jpg')
image=image.convert('L')
threshold = 127#阈值
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image=image.point(table,'1')
image.show()
print(tesserocr.image_to_text(image))


import tesserocr
from PIL import Image
image=Image.open('test.jpg')
print(tesserocr.image_to_text(image))
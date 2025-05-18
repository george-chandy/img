from PIL import Image
import pytesseract

img = Image.open("sample_images/1.jpeg")
text = pytesseract.image_to_string(img)
print(text)
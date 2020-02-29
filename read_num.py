from PIL import Image,ImageOps,ImageFilter
import pyocr
import pyocr.builders

def read_num():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print('No OCR tool found')
    tool = tools[0]
    img = 'image/prime.png'
    img = Image.open(img).convert('RGB')
    img_convert = ImageOps.invert(img) #白黒反転で精度向上
    number = tool.image_to_string(
        img_convert,
        lang='eng',
        builder = pyocr.builders.TextBuilder(tesseract_layout=7)
    )
    try:
        int(number.replace(' ',''))
        return(int(number.replace(' ','')))
    except ValueError:
        print(number)
        return 'error'
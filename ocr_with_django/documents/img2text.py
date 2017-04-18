import sys
from PIL import Image, ImageFilter, ImageEnhance
from tesserocr import PyTessBaseAPI



def convert(path):
    with PyTessBaseAPI(init=True) as api:
        with Image.open('akbar.png') as image:
            api.End()
            # setting language to English and Engine to TESSERACT_CUBE_COMBINED
            # language libraries have to be added to /usr/local/Cellar/tesseract/3.05.00/share/tessdata/
            api.Init(lang='eng', oem=2)
            #new_image = image.convert('1')
            enh = ImageEnhance.Sharpness(image)
            new_image = enh.enhance(2)
            #filtered_image = image.filter(ImageFilter.CONTOUR)
            #sharpened_image = image.filter(ImageFilter.SHARPEN)
            api.SetImage(new_image)
            api.Recognize()
            utf8_text = api.GetUTF8Text()
            #new_image.save('new.png', 'PNG')
            it = api.AnalyseLayout()
            orientation, direction, order, deskew_angle = it.Orientation()
            print "Orientation: {:d}".format(orientation)
            print "WritingDirection: {:d}".format(direction)
            print "TextlineOrder: {:d}".format(order)
            print "Deskew angle: {:.4f}".format(deskew_angle)
            print api.GetInitLanguagesAsString()
            print api.GetThresholdedImageScaleFactor()
    return utf8_text


print convert(sys.argv[1:])



from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt


from PIL import Image, ImageFilter, ImageEnhance
from tesserocr import PyTessBaseAPI
from models import SWTScrubber

class OcrFormView(TemplateView):
    template_name = 'documents/ocr_form.html'
ocr_form_view = OcrFormView.as_view()


class OcrView(View):
    def post(self, request, *args, **kwargs):
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                new_image = image.convert('1')
                enh = ImageEnhance.Contrast(image)
                enh_image = enh.enhance(1.3)
                filtered_image = image.filter(ImageFilter.CONTOUR)
                sharpened_image = image.filter(ImageFilter.SHARPEN)
                api.SetImage(image)
                utf8_text = api.GetUTF8Text()
                new_image.save('new.png', 'PNG')
        return JsonResponse({'utf8_text': utf8_text})
ocr_view = csrf_exempt(OcrView.as_view())

import base64
import logging
import numpy as np
import os
from pathlib import Path
from cv2 import cv2

from django.http import JsonResponse
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# from ai_endpoint.forms import ProfileForm
ROOT_STORED_IMAGES = os.environ["RACAS_IMAGES_ROOT"]


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#
# def upload_image(request):
#     saved = True
#     if request.method == "POST":
#         # Get the posted form
#         profile_form = ProfileForm(request.POST, request.FILES)
#
#         if profile_form.is_valid():
#             pass
#
#     else:
#         profile_form = ProfileForm()
#
#     return render(request, 'saved.html', locals())

# def b64e(s):
#     return base64.b64encode(s.encode()).decode()


def b64d(s):
    return base64.b64decode(s).decode()


def from_base64(base64_data):
    np_arr = np.fromstring(base64_data.decode('base64'), np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_ANYCOLOR)


@csrf_exempt
def ajax_view(request):
    data = {
        "msg": "No file attached",
    }

    if request.method == 'POST':
        # logging.log(level=logging.CRITICAL, msg=f"Keys found: {request.POST.keys()}")
        if "project_ref" in request.POST.keys():
            project_ref = request.POST["project_ref"]
            dst_folder = Path(ROOT_STORED_IMAGES) / project_ref
            dst_folder.mkdir(exist_ok=True, parents=True)
            logging.log(level=logging.CRITICAL, msg=f"Project_ref: {project_ref}")
        else:
            logging.log(level=logging.CRITICAL, msg="No 'project_ref' key found in post.")
            return JsonResponse({"msg": "No 'project_identifier' key found in post."})

        if hasattr(request, "FILES"):
            in_memory_uploaded_file = dict(request.FILES)["image"][0]  # request.FILES.get('image')
            content_type = in_memory_uploaded_file.content_type
            size = in_memory_uploaded_file.size
            charset = in_memory_uploaded_file.charset
            content_type_extra = in_memory_uploaded_file.content_type_extra

            file_name = in_memory_uploaded_file.name
            dst_file_path = dst_folder / file_name
            with open(str(dst_file_path), 'wb+') as destination:
                for chunk in in_memory_uploaded_file.chunks():
                    destination.write(chunk)
            # Subprocess call here to detect.py in yoloV5.
            # if annotations.txt:
            #    detections = read lines annotations.txt file into list.
            # else:
            detections = []
            data = {
                "detections": detections,
            }
            logging.log(level=logging.INFO, msg=f"{file_name} {size}")

    return JsonResponse(data)

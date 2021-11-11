import logging
import os
from pathlib import Path

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


ROOT_STORED_IMAGES = os.environ["RACAS_IMAGES_ROOT"]


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
            return JsonResponse({"error": "No 'project_identifier' key found in post."})

        if "classifier" in request.POST.keys():
            if request.POST["classifier"] == "sealed_road_defects":
                model_path = Path("/home/david/addn_repos/yolov5/runs/train")
            else:
                msg = "Nominated classifier is unknown"
                logging.log(level=logging.CRITICAL, msg=msg)
                return JsonResponse({"error": msg})
        else:
            msg = "No 'classifier' key found in post."
            logging.log(level=logging.CRITICAL, msg=msg)
            return JsonResponse({"error": msg})

        if "model_version" in request.POST.keys():
            model_path = model_path / "Collation_6_unweighted_equal_fitness_scale50pcnt"
        else:
            msg = "No 'model_version' key found in post."
            logging.log(level=logging.CRITICAL, msg=msg)
            return JsonResponse({"error": msg})

        model_path = model_path / "weights" / "best.pt"

        if hasattr(request, "FILES"):
            in_memory_uploaded_file = dict(request.FILES)["image"][0]  # request.FILES.get('image')
            size = in_memory_uploaded_file.size
            file_name = in_memory_uploaded_file.name
            dst_file_path = dst_folder / file_name
            with open(str(dst_file_path), 'wb+') as destination:
                for chunk in in_memory_uploaded_file.chunks():
                    destination.write(chunk)

            run_name = "tmp"
            tmp_folder = Path("/home/david/addn_repos/yolov5/runs/detect") / run_name
            tmp_folder.unlink(missing_ok=True)
            tmp_folder.mkdir(parents=True)

            cmd = [
                "/home/david/addn_repos/yolov5/venv/bin/python",
                "/home/david/addn_repos/yolov5/detect.py",
                "--source",
                str(dst_file_path),
                "--iou-thres",
                0.5,
                "--agnostic-nms",
                "--max-det",
                "20",
                "--nosave",
                # "--img",
                # "640",
                "--device",
                1,
                "--conf-thres",
                0.2,
                "--weights",
                str(model_path),
                "--name",
                run_name,
                # "--save-txt",
                # "--save-crop",
                # "--save-conf"
            ]
            result = subprocess.run(cmd)
            tmp_results = tmp_folder / "results.txt"
            if tmp_results.exists():
                with open(str(tmp_results), "r") as tmp_file:
                    detections = tmp_file.readlines()
            else:
                msg = "No results.txt file found"
                logging.log(level=logging.CRITICAL, msg=msg)
                return JsonResponse({"error": msg})

            # tmp_folder.unlink()

            data = {
                "detections": detections,
            }
            logging.log(level=logging.INFO, msg=f"{file_name} {type(result)}")

    return JsonResponse(data)

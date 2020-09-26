# -*- coding: utf-8 -*-
from django.http import HttpResponse
from ehall.Recive import Recive
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def api(request):
    Rec = Recive(request)
    res = Rec.run()
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")
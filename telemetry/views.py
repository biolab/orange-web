import logging

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger()


@csrf_exempt
def v1(request):
    try:
        telemetry = dict(request.POST)
        for key, value in telemetry.items():
            if type(value) == list:
                telemetry[key] = value[0]

        if len(telemetry):
            with open("telemetry.json", 'a+') as fp:
                json.dump(telemetry, fp)
                fp.write("\n")
    except Exception as e:
        log.exception("Saving failed.", exc_info=e)

    return HttpResponse(json.dumps(dict(status='ok')),
                        content_type="application/json")
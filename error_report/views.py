import json
import logging
import os

from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger(__file__)


def _cleanup(path):
    return os.path.abspath(os.path.join('/', path))[1:]


@csrf_exempt
def v1(request):
    version = request.POST.get("Version", "unknown")
    widget_module = request.POST.get("Widget Module", "unknown")
    widget_module, colon, lineno = widget_module.rpartition(":")
    module = request.POST.get("Module", "unknown")
    path = _cleanup(os.path.join(widget_module, version, module))
    path = os.path.join(settings.ERROR_REPORT_DIR, path)
    try:
        os.makedirs(path)
    except OSError:
        pass
    timestamp = datetime.now().isoformat()

    workflow = request.POST.get("Widget Scheme", None)
    if workflow:
        workflow_file = "{}.ows".format(timestamp)
        with open(os.path.join(path, workflow_file), 'w') as f:
            f.write(workflow)

    report = dict(request.POST)
    report.pop("Widget Scheme", None)
    report["Stack Trace"] = request.POST.get("Stack Trace").split('\n')
    report_file = "{}.txt".format(timestamp)
    with open(os.path.join(path, report_file), 'w') as f:
        json.dump(report, f, sort_keys=True, indent=4)

    return HttpResponse(json.dumps(dict(status='ok')),
                        content_type="application/json")

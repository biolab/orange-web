import logging
import re
import uuid

from raven import Client

logger = logging.getLogger(__name__)

PYTHON_FOLDERS = [
    "site-packages",
    "dist-packages",
    "Python34.lib",
    "anaconda3.lib",
    "lib.python3.4",
    "orange3"
]
FRAMES_RE = re.compile('File "([^"]+)", line (\d+), in ([^ ]+) (.*)')
DEVICE_RE = re.compile('Python ([\d\.]+) on ([^ ]+) ([^ ]+) (.+) ([^ ]+)$')


def guess_module(filename):
    file_module = filename.replace("\\\\", "\\").replace("/", ".").replace("\\", ".")

    for f in PYTHON_FOLDERS:
        base, prefixed, module = file_module.partition(f + ".")
        if not prefixed:
            continue

        for ext in [".py", ".__init__"]:
            if module.endswith(ext):
                module = module[:-len(ext)]
        return module


def extract_frames(stack_trace):
    if isinstance(stack_trace, list):
        stack_trace = "\n".join(stack_trace)
    frames = FRAMES_RE.findall(stack_trace)
    return [dict(lineno=lineno,
                 function=function,
                 filename=fn if guess_module(fn) is None else None,
                 module=guess_module(fn),
                 context_line=line)
            for fn, lineno, function, line in frames]


def get_device_info(env):
    if isinstance(env, list):
        env = "".join(list).strip()
    device_info = DEVICE_RE.findall(env)
    for py_version, os, os_version, os_build, machine in device_info:
        return dict(os=dict(name=os,
                            version=os_version,
                            build=os_build),
                    runtime=dict(name="python",
                                 version=py_version))


def get_exception(ex, st):
    if isinstance(ex, list):
        ex = "".join(ex)
    exc_type, _, exc_message = ex.partition(":")
    return dict(
        values=[
            dict(
                stacktrace=dict(
                    frames=extract_frames(st)
                ),
                type=exc_type,
                value=exc_message,
            )
        ]
    )


def get_version(v):
    if isinstance(v, list):
        v = " ".join(v)
    return v.partition("0+")[0]


def create_sentry_report(report):
    if "Exception" not in report:
        return {}

    module = report["Module"][0]
    widget_module = report.get("Widget Module", [""])[0]
    culprit = widget_module or module
    machine_id = report["Machine ID"][0]
    packages = dict(p.split('==')
                    for p in report.get("Installed Packages", [""])[0].split(', ') if p)
    data = dict(
        event_id=uuid.uuid4().hex,
        platform="python",
        exception=get_exception(report["Exception"], report["Stack Trace"]),
        culprit=culprit,
        release=get_version(report["Version"]),
        user=dict(id=machine_id),
        fingerprint=[module],
        contexts=get_device_info(report["Environment"][0]),
        tags=dict(),
        modules=packages,
    )
    if module.startswith("orangecontrib"):
        m = module.split(".")
        data["tags"]["addon"] = m[1]
    return data


def send_to_sentry(report, dsn):
    sentry_report = create_sentry_report(report)
    if not sentry_report:
        return

    try:
        client = Client(dsn)
        client.send(**sentry_report)
    except Exception as ex:
        # There is nothing we can do if sentry is not available
        logger.exception(ex)

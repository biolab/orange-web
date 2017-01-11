import copy
import logging
import re
import uuid

from django.conf import settings
from raven import Client

logger = logging.getLogger(__name__)

REPORTS_BASE_URL = 'http://butler.fri.uni-lj.si/errors/{}'

PYTHON_FOLDERS = [
    "site-packages",
    "dist-packages",
    "Python34.lib",
    "anaconda3.lib",
    "lib.python3.4",
    "orange3",
    "orangecontrib",
]
FRAMES_RE = re.compile('File "([^"]+)", line (\d+), in ([^ ]+) (.*)')
DEVICE_RE = re.compile('Python ([\d\.]+) on ([^ ]+) ([^ ]+) (.+) ([^ ]+)$')


def guess_module(filename):
    file_module = filename.replace("\\\\", "\\").replace("/", ".").replace("\\", ".")

    for f in PYTHON_FOLDERS:
        base, prefixed, module = file_module.partition(f + ".")
        if not prefixed:
            continue

        # fix for addons in dev mode; `orangecontrib.` is part of module
        if f == 'orangecontrib':
            module = prefixed + module

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


def get_dsn(name):
    dsn = "ERROR_REPORT_SENTRY_DSN_{}".format(name.upper())
    return getattr(settings, dsn, None)


def prep_addon_data(addon, data, duplicated):
    # make a copy so we can have different tags
    addon_data = copy.deepcopy(data)

    # flag duplication status
    data["tags"]["addon"] = addon
    data["tags"]["duplicated_in_addon"] = duplicated
    addon_data["tags"]["duplicated_in_core"] = duplicated

    # replace release with addon version
    addon_data["tags"]["orange_version"] = data['release']
    addon_data["release"] = "unknown"
    for package, version in addon_data['modules'].items():
        package = package.lower()
        if 'orange' in package and addon in package:
            addon_data['release'] = get_version(version)
    return addon_data


def get_dsn_report_pairs(sentry_report):
    frames = sentry_report['exception']['values'][0]['stacktrace']['frames']
    modules = [f['module'] for f in frames if f.get('module') not in
               (None, '', 'Orange.canvas.scheme.widgetsscheme')]

    def _filter_modules(names):
        return [m for m in modules
                if m and any(m.startswith(n) for n in names)]

    core_calls = _filter_modules(['Orange.'])
    addon_calls = _filter_modules(['orangecontrib.'])
    last_in_addon = _filter_modules(['Orange.', 'orangecontrib.'])
    last_in_addon = last_in_addon and last_in_addon[-1] in addon_calls

    addon, addon_dsn = None, None
    if any(addon_calls):
        addon = addon_calls[0].split('.')[1]
        addon_dsn = get_dsn(addon)

    if any(addon_calls) and addon_dsn:
        # errors whose stacktrace contains call from addon & core and the
        # last call does not come from addon are sent to both issue trackers
        duplicated = any(core_calls) and not last_in_addon

        yield addon_dsn, prep_addon_data(addon, sentry_report, duplicated)
        if duplicated:
            yield get_dsn('ORANGE'), sentry_report
    else:
        sentry_report["tags"]["duplicated_in_addon"] = 'False'
        yield get_dsn('ORANGE'), sentry_report


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
        extra={'Schema Url': schema_url, }
    )
    return data


def send_to_sentry(report):
    sentry_report = create_sentry_report(report)
    if not sentry_report:
        return

    for dsn, report in get_dsn_report_pairs(sentry_report):
        try:
            client = Client(dsn)
            client.send(**report)
        except Exception as ex:
            # There is nothing we can do if sentry is not available
            logger.exception(ex)

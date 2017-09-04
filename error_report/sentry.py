import copy
import logging
import re
import uuid

from django.conf import settings
from raven import Client

logger = logging.getLogger(__name__)

REPORTS_BASE_URL = 'http://qa.orange.biolab.si/errors/{}'

PYTHON_FOLDERS = [
    "site-packages",
    "dist-packages",
    "Python34.lib",
    "anaconda3.lib",
    "lib.python3.4",
    "orange3",
]

ORANGE_ADDONS = [
    'orangecontrib',
    'lekbf',
    '_textable',
    'orangebiodepot',
]

FRAMES_RE = re.compile('File "([^"]+)", line (\d+), in ([^ ]+) (.*)')
DEVICE_RE = re.compile('Python ([\d\.]+) on ([^ ]+) ([^ ]+) (.+) ([^ ]+)$')

# Modules that should not be grouped by
GENERAL_MODULES = [
    "Orange.data.domain:232",        # domain.index(attr_name)
    "sklearn.utils.validation:424",  # check_array
    "Orange.util:141",               # attrgetter(attr)(obj)
    "Orange.statistics.util:52",     # bincount
]

ORANGE3_DATASETS = ('Orange3-Datasets', "https://2cb16c369f474e799ae384045dbf489e:b35f4e39d8b1417190aeb475e8c3df0a@sentry.io/167538")
DSN_3RDPARTY = "https://d077c44bbab1407595c9838ace02aea5:f3f434118ea44e0a9e61c580ca156505@sentry.io/176069"
DSN_TEXTABLE = "https://489e53f2068441f48d0d7bb3f5f066d5:299379ad47a140dfaee2042a6bb4204f@sentry.io/207453"

DSN_ORANGE = "https://6f0311046ad2438598ae121cdabd878f:df101b5249ea4c89a82fc1f5da73886d@sentry.io/124497"
# For addons with separate DSNs mapping from namespace to addon name
# must be provided for reporting addon version as release.
NAMESPACE_TO_ADDON = {
    'associate':        ('Orange3-Associate', "https: // cde61b47c74c4f98931264c1112b1bc2:10cfb3b76a16466fb6583a7952c660a8@sentry.io/167541"),
    'bio':              ('Orange-Bioinformatics', "https://ddadbc7a4cdd4b32a6f7f15eb2ca991e:8858577a9d214f56a0a9e3c571b2ec5d@sentry.io/167549"),
    'conformal':        ('Orange3-Conformal-Prediction', "https://3cf0bca1e5ed4b6a811c9980f27ed8ee:94015ed538b04bdcb4da2c35f0d792f8@sentry.io/167539"),
    'datafusion':       ('Orange3-DataFusion', "https://894bd2e1f47a4271834b8fbc019fc90b:e9d52ebb81354ca0b84fa64624f3882a@sentry.io/167542"),
    'wbd':              ORANGE3_DATASETS,
    'datasets':         ORANGE3_DATASETS,
    'educational':      ('Orange3-Educational', "https://93323bc17a094974a830b25abbae01b5:4fd5e7c529e34afd97ceca08ed4f059d@sentry.io/167545"),
    'geo':              ('Orange3-Geo', "https://f3b7d23593d14247808b70ff964b3956:ff25c1d23d3a4eca849429c731c874d9@sentry.io/167528"),
    'imageanalytics':   ('Orange3-ImageAnalytics', "https://cc2ef6171aad4b6ba344e2851169db7d:cd21ed3e80ae4f4385b31a24e0d036cf@sentry.io/161064"),
    'network':          ('Orange3-Network', "https://14706c0ff3e047d999cff64e6100eb25:1dd7b84d0afc449abba1757e3520b0c2@sentry.io/167534"),
    'prototypes':       ('Orange3-Prototypes', "https://d7440097e7f64e4cbff90dd31fc8876e:dde09f7ba917431884b7eb04c814b824@sentry.io/167530"),
    'recommendation':   ('Orange3-Recommendation', "https://e447ddb4e80149289bca679121359c03:e4b9a0f1a1414f7d906e56b8e28be9cc@sentry.io/167543"),
    'text':             ('Orange3-Text', "https://38ffabded40c46b9952b2acebc726866:147d6a5becfa40499b6d79e858fb6ef1@sentry.io/128443"),
    'timeseries':       ('Orange3-Timeseries', "https://e8f30f9dbaf74635bb10e37abe0b5354:2478a41e2f95463db8ceebfeb060cc99@sentry.io/161065"),
    'testing':          ('', "https://261797e8fa4544ffb931bc495157d2e3:44e30b93f9f1463a975725f82ca18039@sentry.io/128442"),
    'lekbf':            ('lekbf', "https://7da121cc693045c688d5ffd2d320e65b:1e2b3e613c85437ba8f005035572b3b7@sentry.io/174357"),
    'infrared':         ('Orange-Infrared', "https://1cb3697dbfc04f748bae548865f1b1a8:eb0b726e492b44358a277c97c8c631f2@sentry.io/176038"),
    'spark':            ('Orange3-spark', DSN_3RDPARTY),
    'textable_prototypes': ('Orange3-Textable-Prototypes', DSN_TEXTABLE),
    'orangebiodepot':   ('orangebiodepot', DSN_3RDPARTY),
    '_textable':        ('Orange3-Textable', DSN_TEXTABLE),
    'variants':         ('Orange3-Variants', "https://3acf738fd9a3458ab76cabcfaa072dcf:6b24664b8a67412382986cd388de965b@sentry.io/209789"),
}


def guess_module(filename):
    file_module = filename.replace("\\\\", "\\").replace("/", ".").replace("\\", ".")

    for f in PYTHON_FOLDERS + ORANGE_ADDONS:
        base, prefixed, module = file_module.partition(f + ".")
        if not prefixed:
            continue

        # fix for addons in dev mode; e.g `orangecontrib.` belongs to module
        if f in ORANGE_ADDONS:
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


def get_dsn(name, prefix=None):
    if name.upper() == "ORANGE":
        return DSN_ORANGE
    elif name in NAMESPACE_TO_ADDON:
        return NAMESPACE_TO_ADDON[name][1]
    elif prefix in NAMESPACE_TO_ADDON:
        return NAMESPACE_TO_ADDON[prefix][1]
    else:
        return NAMESPACE_TO_ADDON["testing"][1]


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
    if addon in NAMESPACE_TO_ADDON:
        addon = NAMESPACE_TO_ADDON[addon][0]
        for package, version in addon_data['modules'].items():
            if addon == package:
                addon_data['release'] = get_version(version)
                break
    return addon_data


def get_dsn_report_pairs(sentry_report):
    logger.info("Getting DNS report pairs.")
    frames = sentry_report['exception']['values'][0]['stacktrace']['frames']
    modules = [f['module'] for f in frames if f.get('module') not in
               (None, '', 'Orange.canvas.scheme.widgetsscheme')]

    def _filter_modules(names):
        return [m for m in modules
                if m and any(m.startswith(n + '.') for n in names)]

    core_calls = _filter_modules(['Orange'])
    addon_calls = _filter_modules(ORANGE_ADDONS)
    last_in_addon = _filter_modules(['Orange'] + ORANGE_ADDONS)
    last_in_addon = last_in_addon and last_in_addon[-1] in addon_calls

    addon, prefix, addon_dsn = None, None, None
    if any(addon_calls):
        prefix, addon = addon_calls[0].split('.')[:2]
        addon_dsn = get_dsn(addon, prefix)

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
    packages = report.get("Installed Packages", "")
    if isinstance(packages, list):
        packages = ' '.join(packages)
    packages = dict(p.split('==') for p in packages.split(', ') if p)
    schema_url = report.get("Widget Scheme", "")
    schema_url = REPORTS_BASE_URL.format(schema_url) if schema_url else '<not-provided>'
    data = dict(
        event_id=uuid.uuid4().hex,
        platform="python",
        exception=get_exception(report["Exception"], report["Stack Trace"]),
        culprit=culprit,
        release=get_version(report["Version"]),
        user=dict(id=machine_id),
        contexts=get_device_info(report["Environment"][0]),
        tags=dict(),
        modules=packages,
        extra={'Schema Url': schema_url, }
    )
    if module not in GENERAL_MODULES:
        # group issues by the module of the last frame
        # (unless the last frame is too general)
        data["fingerprint"] = [module]
    info_msg = "Sentry report created."
    if "Exception" in report:
        info_msg += " Exception: {}".format(report["Exception"])
    logger.info(info_msg)
    return data


def send_to_sentry(report):
    sentry_report = create_sentry_report(report)
    if not sentry_report:
        return

    for dsn, report in get_dsn_report_pairs(sentry_report):
        try:
            client = Client(dsn, raise_send_errors=True)
            client.send(**report)
        except Exception as ex:
            # There is nothing we can do if sentry is not available
            logger.exception(ex)
        else:
            logger.info("Report has been sent to sentry.")

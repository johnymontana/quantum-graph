import os

from qgis.gui import QgisInterface

from quantumgraph.qgis_plugin_tools.infrastructure.debugging import setup_debugpy  # noqa F401
from quantumgraph.qgis_plugin_tools.infrastructure.debugging import setup_ptvsd  # noqa F401
from quantumgraph.qgis_plugin_tools.infrastructure.debugging import setup_pydevd  # noqa F401

debugger = os.environ.get("QGIS_PLUGIN_USE_DEBUGGER", "").lower()
if debugger in {"debugpy", "ptvsd", "pydevd"}:
    locals()["setup_" + debugger]()


def classFactory(iface: QgisInterface):  # noqa N802
    from quantumgraph.plugin import Plugin

    return Plugin()

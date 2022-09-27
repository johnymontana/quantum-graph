#! python3  # noqa: E265

"""
    Processing provider module.
"""

# PyQGIS
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon

# project
from quantumgraph.__about__ import DIR_PLUGIN_ROOT, __version__

# ############################################################################
# ########## Classes ###############
# ##################################


class QuantumgraphProvider(QgsProcessingProvider):
    """
        Processing provider class.
    """

    def loadAlgorithms(self):
        """Loads all algorithms belonging to this provider."""
        pass

    def id(self) -> str:
        """Unique provider id, used for identifying it. This string should be unique, \
        short, character only string, eg "qgis" or "gdal". \
        This string should not be localised.

        :return: provider ID
        :rtype: str
        """
        return "quantumgraph"

    def name(self) -> str:
        """Returns the provider name, which is used to describe the provider
        within the GUI. This string should be short (e.g. "Lastools") and localised.

        :return: provider name
        :rtype: str
        """
        return self.tr("Quantumgraph")

    def longName(self) -> str:
        """Longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools". This string should be localised. The default
        implementation returns the same string as name().

        :return: provider long name
        :rtype: str
        """
        return self.tr("QuantumGraph - Tools")

    def icon(self) -> QIcon:
        """QIcon used for your provider inside the Processing toolbox menu.

        :return: provider icon
        :rtype: QIcon
        """
        return QIcon(str(DIR_PLUGIN_ROOT / "resources/images/default_icon.png"))

    def tr(self, message: str) -> str:
        """Get the translation for a string using Qt translation API.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: str
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate(self.__class__.__name__, message)

    def versionInfo(self) -> str:
        """Version information for the provider, or an empty string if this is not \
        applicable (e.g. for inbuilt Processing providers). For plugin based providers, \
        this should return the plugin’s version identifier.

        :return: version
        :rtype: str
        """
        return __version__

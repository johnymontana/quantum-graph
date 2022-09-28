__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import pytest

from ..tools.exceptions import QgsPluginNetworkException
from ..tools.network import download_to_file, fetch


def test_fetch(qgis_new_project):
    data_model = fetch("https://www.gispo.fi/")
    assert len(data_model) > 10000


def test_fetch_invalid_url(qgis_new_project):
    with pytest.raises(QgsPluginNetworkException):
        fetch("invalidurl")


def test_fetch_params(qgis_new_project):
    data_model = fetch("https://www.gispo.fi/", params={"foo": "bar"})
    assert len(data_model) > 10000


@pytest.mark.skip(
    "file does not exist. "
    "TODO: search another file to be used using Content-Disposition"
)
def test_download_to_file(qgis_new_project, tmpdir):
    path_to_file = download_to_file(
        "https://twitter.com/gispofinland/status/1324599933337567232/photo/1",
        tmpdir,
        "test_file",
    )
    assert path_to_file.exists()
    assert path_to_file.is_file()


@pytest.mark.skip(
    "file does not exist. "
    "TODO: search another file to be used using Content-Disposition"
)
def test_download_to_file_without_requests(qgis_new_project, tmpdir):
    path_to_file = download_to_file(
        "https://twitter.com/gispofinland/status/1324599933337567232/photo/1",
        tmpdir,
        "test_file",
        use_requests_if_available=False,
    )
    assert path_to_file.exists()
    assert path_to_file.is_file()


def test_download_to_file_with_name(qgis_new_project, tmpdir):
    path_to_file = download_to_file(
        "https://raw.githubusercontent.com/GispoCoding/FMI2QGIS/master/FMI2QGIS/test/data/aq_small.nc",  # noqa E501
        tmpdir,
    )
    assert path_to_file.exists()
    assert path_to_file.is_file()
    assert path_to_file.name == "aq_small.nc"


def test_download_to_file_invalid_url(qgis_new_project, tmpdir):
    with pytest.raises(QgsPluginNetworkException):
        download_to_file("invalidurl", tmpdir)


def test_download_to_file_invalid_url_without_requests(qgis_new_project, tmpdir):
    with pytest.raises(QgsPluginNetworkException):
        download_to_file("invalidurl", tmpdir)

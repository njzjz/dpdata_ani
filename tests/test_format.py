import dpdata
import requests


def test_load_ani1x(tmp_path):
    # download ani1x to fn
    url = "https://figshare.com/ndownloader/files/18112775"
    r = requests.get(url)
    fn = tmp_path / "ani.h5"
    with open(fn, 'wb') as fw:
        fw.write(r.content)
    # dpdata
    ms = dpdata.MultiSystems().from_ani_1x(fn)
    assert len(ms)

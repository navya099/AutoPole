from polefactory import PoleTESTFctory
from core.WIRE.wire_manager import WireManager

def test_wiremanager_simple():
    poletester = PoleTESTFctory()
    poletester.run(2,10)
    mgr = WireManager(None, poletester.collection)
    mgr.run()

    assert mgr.wiredata is not None
    assert len(mgr.wiredata.bundles) == 20

test_wiremanager_simple()

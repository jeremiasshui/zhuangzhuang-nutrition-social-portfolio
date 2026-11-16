import tempfile, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_asset import check

class AssetChecks(unittest.TestCase):
    def test_good(self):
        self.assertEqual(check(ROOT/'examples/good-threads.md'), [])
    def test_guarantee(self):
        f=check(ROOT/'examples/bad-guarantee.md')
        self.assertTrue(any('保證' in x or '承諾' in x for x in f))
    def test_double_cta(self):
        f=check(ROOT/'examples/bad-double-cta.md')
        self.assertTrue(any('CTA' in x for x in f))

if __name__=='__main__': unittest.main()

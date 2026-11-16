import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_copy import check_dir  # 接縫：唯一被測的介面

PLATFORMS = ("shorts", "threads", "fb", "xhs")

def valid_body(platform):
    if platform == "shorts":
        return "\n## 開場\n先吃菜。\n\n## 主體\n再吃肉。【待營養師確認】\n\n## 重點整理\n順序。\n\n## 行動引導\n留言『烤肉』。\n"
    if platform == "xhs":
        return "\n## 封面標題\n烤肉順序\n\n## 正文\n先吃菜再吃肉。\n\n## 標籤\n#烤肉\n"
    return "\n先吃菜再吃肉。留言『烤肉』。\n"

def valid_file(platform, n, body=None):
    head = f"# S{n}｜標題｜{platform}\n回合：1\n本輪修改：初稿\n"
    return head + (body if body is not None else valid_body(platform))

class Fixture:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
    def fill(self, skip=(), override=None):
        for p in PLATFORMS:
            (self.root / p).mkdir()
            for n in range(1, 10):
                if (p, n) in skip: continue
                text = override.get((p, n)) if override and (p, n) in override else valid_file(p, n)
                (self.root / p / f"S{n}.md").write_text(text, encoding="utf-8")
        return self.root

class Base(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture(); self.addCleanup(self.fx.tmp.cleanup)

class K1FileCount(Base):
    def test_all_36_files_pass(self):
        rep = check_dir(self.fx.fill())
        self.assertTrue(rep.ok, rep.failures)

    def test_missing_s9_in_shorts_is_reported(self):
        rep = check_dir(self.fx.fill(skip={("shorts", 9)}))
        self.assertFalse(rep.ok)
        f = rep.failures[0]
        self.assertEqual((f.platform, f.rule), ("shorts", "K1"))
        self.assertIn("S9.md", f.message)

if __name__ == "__main__":
    unittest.main()

class K2Header(Base):
    def test_wrong_platform_in_title_line(self):
        bad = "# S3｜標題｜threads\n回合：1\n本輪修改：初稿\n" + valid_body("shorts")
        rep = check_dir(self.fx.fill(override={("shorts", 3): bad}))
        f = [x for x in rep.failures if x.rule == "K2"]
        self.assertEqual((f[0].platform, f[0].script), ("shorts", "S3"))
        self.assertIn("第 1 行", f[0].message)

    def test_missing_round_line(self):
        bad = "# S3｜標題｜shorts\n本輪修改：初稿\n" + valid_body("shorts")
        rep = check_dir(self.fx.fill(override={("shorts", 3): bad}))
        self.assertTrue(any(x.rule == "K2" and "第 2 行" in x.message for x in rep.failures))

class K3HardGuardrails(Base):
    def _fail_msgs(self, platform, body):
        rep = check_dir(self.fx.fill(override={(platform, 5): valid_file(platform, 5, body)}))
        return [x.message for x in rep.failures if x.rule == "K3" and x.script == "S5"]

    def test_guarantee_word_fails(self):
        msgs = self._fail_msgs("fb", "\n保證一個月瘦。留言『月餅』。\n")
        self.assertTrue(any("保證" in m for m in msgs))

    def test_calorie_word_daka_fails(self):
        msgs = self._fail_msgs("threads", "\n一顆 300 大卡。留言『月餅』。\n")
        self.assertTrue(any("大卡" in m for m in msgs))

    def test_calorie_word_kcal_fails(self):
        msgs = self._fail_msgs("threads", "\n一顆 300 kcal。留言『月餅』。\n")
        self.assertTrue(any("kcal" in m for m in msgs))

    def test_supplement_recommendation_fails(self):
        msgs = self._fail_msgs("fb", "\n推薦這款保健食品。留言『月餅』。\n")
        self.assertTrue(msgs)

    def test_header_mentioning_guarantee_is_not_body(self):
        # 檔頭「本輪修改」引用審稿意見時可能出現「保證」二字，正文沒有就應通過
        head = "# S5｜標題｜fb\n回合：2\n本輪修改：依 reviewer-brand 對「保證瘦」的意見，改為「因人而異」\n"
        rep = check_dir(self.fx.fill(override={("fb", 5): head + valid_body("fb")}))
        self.assertFalse([x for x in rep.failures if x.rule == "K3"])

class K4WordCount(Base):
    def _k4(self, platform, body):
        rep = check_dir(self.fx.fill(override={(platform, 2): valid_file(platform, 2, body)}))
        return [x for x in rep.failures if x.rule == "K4" and x.script == "S2"]

    def test_threads_301_chars_fails_300_passes(self):
        # 規格：threads ≤ 300（SDD §9）。用獨立算出的長度，不用程式自己算。
        self.assertTrue(self._k4("threads", "\n" + "字" * 301 + "\n"))
        self.fx = Fixture(); self.addCleanup(self.fx.tmp.cleanup)
        self.assertFalse(self._k4("threads", "\n" + "字" * 300 + "\n"))

    def test_annotations_are_not_counted(self):
        body = "\n" + "字" * 300 + "【待營養師確認】" * 5 + "\n"
        self.assertFalse(self._k4("threads", body))

    def test_shorts_counts_only_four_segments(self):
        seg = "\n## 開場\n" + "字" * 100 + "\n\n## 主體\n" + "字" * 100 + "\n\n## 重點整理\n" + "字" * 30 + "\n\n## 行動引導\n" + "字" * 30 + "\n\n## Shorts 標題\n" + "字" * 25 + "\n\n## 字幕標注\n" + "字" * 200 + "\n"
        self.assertFalse(self._k4("shorts", seg))  # 四段共 260，標題與字幕標注不計

    def test_xhs_counts_only_main_text(self):
        body = "\n## 封面標題\n" + "字" * 20 + "\n\n## 要點卡\n" + "字" * 200 + "\n\n## 正文\n" + "字" * 301 + "\n\n## 標籤\n#a\n"
        self.assertTrue(self._k4("xhs", body))
        self.fx = Fixture(); self.addCleanup(self.fx.tmp.cleanup)
        body_ok = "\n## 封面標題\n" + "字" * 20 + "\n\n## 要點卡\n" + "字" * 200 + "\n\n## 正文\n" + "字" * 300 + "\n\n## 標籤\n#a\n"
        self.assertFalse(self._k4("xhs", body_ok))

class K5SingleCTA(Base):
    def _k5(self, body):
        rep = check_dir(self.fx.fill(override={("fb", 7): valid_file("fb", 7, body)}))
        return [x for x in rep.failures if x.rule == "K5" and x.script == "S7"]

    def test_comment_and_line_together_fail(self):
        self.assertTrue(self._k5("\n留言『五階段』，或加 LINE https://lin.ee/z8FXY7v 預約。\n"))

    def test_two_line_links_fail(self):
        self.assertTrue(self._k5("\n加 LINE https://lin.ee/z8FXY7v。再一次 https://lin.ee/z8FXY7v。\n"))

    def test_single_line_link_passes(self):
        self.assertFalse(self._k5("\n想從第一階段開始，LINE 預約 https://lin.ee/z8FXY7v。\n"))

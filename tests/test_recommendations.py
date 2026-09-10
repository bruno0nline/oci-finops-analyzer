import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from finops_recommendations import recommend
from oci_metrics_cpu_mem_media_ndays import get_regions


def sample(**changes):
    row = dict(shape="VM.Standard.E4.Flex", ocpus=3, memory_gb=30,
               cpu_p95_percent=72.95, mem_p95_percent=56.2,
               cpu_start_utc="2026-08-10T00:00:00+00:00", mem_start_utc="2026-08-10T00:00:00+00:00",
               end_utc="2026-09-09T00:00:00+00:00", metric_interval="5m", cpu_samples=8640, mem_samples=8640)
    row.update(changes)
    return row


class RecommendationsTests(unittest.TestCase):
    def test_real_memory_regression(self):
        result = recommend(sample())
        self.assertEqual(result["proposed_memory_gb"], 23)
        self.assertEqual(result["proposed_ocpus"], 3)
        self.assertLessEqual(result["projected_mem_p95_percent"], 75)

    def test_upscale_only_pressured_dimension(self):
        cpu = recommend(sample(ocpus=2, memory_gb=32, cpu_p95_percent=99.47, mem_p95_percent=53.92))
        self.assertEqual((cpu["proposed_ocpus"], cpu["proposed_memory_gb"]), (3, 32))
        mem = recommend(sample(ocpus=2, memory_gb=60, cpu_p95_percent=36.96, mem_p95_percent=88.4))
        self.assertEqual((mem["proposed_ocpus"], mem["proposed_memory_gb"]), (2, 71))

    def test_missing_sparse_and_invalid_data_block_proposals(self):
        for changes in [dict(cpu_samples=2052), dict(mem_samples=0), dict(cpu_p95_percent=float("nan")), dict(memory_gb=None), dict(collection_error="denied")]:
            with self.subTest(changes=changes):
                result = recommend(sample(**changes))
                self.assertEqual(result["finops_recommendation"], "INSUFFICIENT_DATA")
                self.assertIsNone(result["proposed_memory_gb"])

    def test_fixed_burstable_and_limits_require_review(self):
        for changes in [dict(shape="VM.Standard.E2.1"), dict(burstable_enabled="YES"), dict(ocpus=64, cpu_p95_percent=99)]:
            self.assertEqual(recommend(sample(**changes))["finops_recommendation"], "REVIEW")

    def test_memory_ratio_preserves_cpu_capacity(self):
        result = recommend(sample(ocpus=8, memory_gb=512, cpu_p95_percent=1, mem_p95_percent=70))
        self.assertGreaterEqual(result["proposed_ocpus"] * 64, result["proposed_memory_gb"])

    def test_default_scope(self):
        self.assertEqual(get_regions(), ["sa-saopaulo-1", "sa-vinhedo-1"])

    def test_word_uses_canonical_target(self):
        import tempfile
        from docx import Document
        from oci_metrics_cpu_mem_word_report import generate_report
        row = sample(instance_name="synthetic", region="sa-saopaulo-1", compartment="test", cpu_mean_percent=20, mem_mean_percent=36)
        row.update(recommend(row))
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "report.docx"
            generate_report([row], docx_path=dest)
            text = "\n".join(p.text for p in Document(dest).paragraphs)
            self.assertIn("23.0 GB", text)
            self.assertNotIn("15.0 GB", text)

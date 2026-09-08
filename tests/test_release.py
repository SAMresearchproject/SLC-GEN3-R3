"""Standalone wiring checks against frozen native output, plus process restoration."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from slc_gen2_r4 import open_runtime, verify_sources
from slc_gen2_r4.__main__ import encoded

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests/fixtures"

def fixture(name):
    return json.loads((FIX / name).read_text())

def normal(value):
    return json.loads(encoded(value))

class ReleaseTests(unittest.TestCase):
    def test_source_identity(self):
        self.assertGreater(verify_sources()["verified_files"], 100)

    def test_installed_integration_fixture(self):
        saved = json.loads(gzip.decompress((FIX / "r4_installation.json.gz").read_bytes()))
        with open_runtime() as runtime:
            for step in saved["steps"]:
                with self.subTest(name=step["name"], operation=step["operation"]):
                    actual = runtime.execute(step["operation"], step["payload"])
                    self.assertEqual(normal(actual), step["expected"])

    def test_owner_word_and_chunk_composition(self):
        request = json.loads((ROOT / "examples/word.json").read_text())
        with open_runtime() as runtime:
            result = runtime.execute("GEN2_RUN", request)
            self.assertEqual(normal(result), fixture("owner_word_native.json"))
            history = result["motion"]["roles"][0]["history_summary"]
            body = history["checkpoint"]["body"]
            chunks = []
            for start, end in [(0, 4), (4, 8), (8, 12)]:
                chunks.append(runtime.execute("GEN2_HISTORY_SUMMARY", {
                    "quantity": body["quantity"], "source_binding": body["source_binding"],
                    "points": body["points"][start:end+1], "edges": body["edges"][start:end]}))
            merged = runtime.compose(chunks[0]["checkpoint"], chunks[1]["checkpoint"])
            merged = runtime.compose(merged["checkpoint"], chunks[2]["checkpoint"])
            self.assertEqual(merged, history)
            self.assertEqual(merged["summary"]["maximizing_points"], ["state:2", "state:5"])

    def test_declared_target_weighted_policy(self):
        source = fixture("owner_inverse.json")
        channels = fixture("owner_channels.json")
        with open_runtime() as runtime:
            inverse = runtime.execute("GEN2_INVERSE_OPEN", {
                "blocks": [[1, 2, 3]], "mode": "ABSOLUTE", "observations": [None, None],
                "event_labels": ["W1+"], "initial_states": [[t, 0, 0] for t in range(4)],
                "target": {"kind": "BARRIER"}})
            self.assertEqual(normal(inverse), source)
            request = {"checkpoint": inverse["checkpoint"], "choices": channels["choices"],
                       "weights": channels["weights"]}
            one = runtime.execute("GEN2_OBSERVATION_PLAN", request)
            self.assertEqual(normal(one), fixture("owner_plan.json"))
            policy = runtime.execute("GEN2_OBSERVATION_POLICY_PLAN", dict(request, horizon=2))
            self.assertEqual(normal(policy), fixture("owner_policy.json"))
            self.assertEqual(policy["selected_label"], "PAIR")
            self.assertEqual(policy["selected_metrics"]["expected_reads"], 1)

    def test_fresh_process_continuation_and_cli_custody(self):
        request = json.loads((ROOT / "examples/word.json").read_text())
        word = request["program"]
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            prefix_input, prefix_output = temp / "prefix.json", temp / "prefix_output.json"
            prefix_input.write_bytes(encoded(dict(request, program=word[:4])))
            producer = subprocess.Popen([sys.executable, "-m", "slc_gen2_r4", "run", "GEN2_RUN",
                str(prefix_input), "--output", str(prefix_output), "--receipts", str(temp / "receipts")], cwd=ROOT)
            self.assertEqual(producer.wait(), 0)
            prefix = json.loads(prefix_output.read_text())["motion"]["roles"][0]["history_summary"]
            (temp / "prefix_checkpoint.json").write_bytes(encoded(prefix))
            script = '''
import json, sys
from pathlib import Path
from slc_gen2_r4 import open_runtime
from slc_gen2_r4.__main__ import encoded
t=Path(sys.argv[1]); prefix=json.loads((t/'prefix_checkpoint.json').read_text())
word=json.loads(Path('examples/word.json').read_text())['program']
with open_runtime() as r:
    before=r.execute('GEN2_REUSE_STATS',{})['modules']['history_summary']
    current=r.execute('GEN2_HISTORY_SUMMARY_APPEND',{'checkpoint':prefix['checkpoint'],'points':[],'edges':[]})
    assert current==prefix
    stats=r.execute('GEN2_REUSE_STATS',{})['modules']['history_summary']
    assert before['operations']==0 and stats['checkpoint_edges_revalidated']==4 and stats['new_edges_summarized']==0
    for lo,hi in [(4,8),(8,12)]:
        q=current['checkpoint']['body']['points'][-1]['state']
        native=r.execute('GEN2_RUN',{'blocks':[[1,2,3]],'initial':q,'program':word[lo:hi]})
        points=[{'id':f'state:{lo+j}','state':q,'action':e} for j,(q,e) in enumerate(zip(native['states'],native['contact_profile'])) if j]
        edges=[{'id':f'edge:{i}','before':f'state:{i}','after':f'state:{i+1}','event':word[i]} for i in range(lo,hi)]
        current=r.execute('GEN2_HISTORY_SUMMARY_APPEND',{'checkpoint':current['checkpoint'],'points':points,'edges':edges})
    expected=json.loads(Path('tests/fixtures/owner_word_native.json').read_text())['motion']['roles'][0]['history_summary']
    assert json.loads(encoded(current))==expected
    (t/'restored.json').write_bytes(encoded(current))
'''
            consumer = subprocess.Popen([sys.executable, "-c", script, str(temp)], cwd=ROOT)
            self.assertEqual(consumer.wait(), 0)
            self.assertNotEqual(producer.pid, consumer.pid)
            self.assertTrue((temp / "restored.json").is_file())
            for receipt in (temp / "receipts").glob("*/RECEIPT.json"):
                record = json.loads(receipt.read_text())
                self.assertEqual(record["output_sha256"], hashlib.sha256((receipt.parent / "OUTPUT.json").read_bytes()).hexdigest())

    def test_deployment_scope_is_explicit(self):
        with open_runtime() as runtime:
            with self.assertRaisesRegex(ValueError, "separately installed tau"):
                runtime.execute("GEN2_TAU_REPLAY", {})

if __name__ == "__main__":
    unittest.main()

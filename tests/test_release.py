"""Portable R3 wiring, exact source preservation and fresh-process recovery."""
from fractions import Fraction
import hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from slc_gen3_r3 import open_runtime,verify_sources
from slc_gen3_r3.__main__ import encoded
ROOT=Path(__file__).resolve().parents[1]
def normal(x):return json.loads(encoded(x))
class ReleaseTests(unittest.TestCase):
    def test_selected_source_and_compatibility(self):
        from CURRENT_REVISION.runtime import load_slc,record
        from slc_gen2_r4 import open_runtime as old_entry
        self.assertIs(old_entry,open_runtime)
        self.assertEqual(record('SLC')['version'],'SLC-GEN3-R3')
        self.assertTrue(load_slc().__name__.endswith('.gen3_runtime'))
        self.assertGreater(verify_sources()['verified_files'],100)
    def test_owner_word_exact_history_and_r3_logs(self):
        payload=json.loads((ROOT/'examples/word.json').read_text())
        expected=json.loads((ROOT/'tests/fixtures/owner_word_native.json').read_text())
        with open_runtime() as r:
            result=normal(r.execute('GEN3_EXECUTE',payload))
            for key in ['states','contact_profile','barrier','initial','program']:
                if key in expected:self.assertEqual(result[key],expected[key])
            summary=result['r3']['logarithmic_accumulation']['summary']
            values=list(map(Fraction,result['contact_profile']));up=down=Fraction(1)
            for a,b in zip(values,values[1:]):
                if b>a:up*=b/a
                elif b<a:down*=a/b
            for key,arg in [('U',up),('D',down),('V',up*down),('L',values[-1]/values[0]),('M',max(values)/values[0])]:self.assertEqual(Fraction(summary[key]['argument']),arg)
            account=result['r3']['history_account']
            self.assertEqual(summary['maximizing_points'],[account+':p'+str(i) for i,v in enumerate(values) if v==max(values)])
            self.assertEqual(normal(r.execute('GEN3_EXECUTE',{'program':['W1+']})['initial']),result['states'][-1])
    def test_weighted_policy_from_current_source(self):
        choices=json.loads((ROOT/'tests/fixtures/owner_channels.json').read_text())['choices']
        with open_runtime() as r:
            inv=r.execute('GEN2_INVERSE_OPEN',{'blocks':[[1,2,3]],'mode':'ABSOLUTE','observations':[None,None],'event_labels':['W1+'],'initial_states':[[t,0,0] for t in range(4)],'target':{'kind':'BARRIER'}})
            masses=['1/8','2/8','3/8','2/8'];weights={m['record_id']:masses[m['initial'][0]] for m in inv['members']}
            policy=r.execute('GEN2_OBSERVATION_POLICY_PLAN',{'checkpoint':inv['checkpoint'],'weights':weights,'choices':choices,'horizon':2})
            self.assertEqual(policy['selected_label'],'PAIR');self.assertEqual(policy['selected_metrics']['expected_reads'],1)
    def test_exact_account_cancellation_append_and_history(self):
        points=[{'id':'p'+str(i),'state':{'step':i},'action':x} for i,x in enumerate(['1','2','1','2'])]
        edges=[{'id':'e'+str(i),'before':'p'+str(i),'after':'p'+str(i+1),'event':{'step':i}} for i in range(3)]
        with open_runtime() as r:
            a=r.execute('GEN3_LOG_OPEN',{'account':'a','quantity':{'kind':'SOURCE_ACTION','units':{},'scope':'HISTORY'},'source_binding':{'test':'portable-exact-trace'},'points':points[:3],'edges':edges[:2]})
            for key,arg in [('U','2'),('D','2'),('L','1'),('V','4')]:self.assertEqual(Fraction(a['summary'][key]['argument']),Fraction(arg))
            b=r.execute('GEN3_LOG_APPEND',{'account':'a','points':points[3:],'edges':edges[2:]})
            self.assertEqual(b['summary']['maximizing_points'],['p1','p3']);self.assertEqual(Fraction(b['summary']['V']['argument']),8)
            history=r.execute('GEN3_HISTORY_EXPORT',{'account':'a'})
            self.assertEqual(len(history['points']),4);self.assertEqual(len(history['edges']),3)
    def test_fresh_process_native_checkpoint_and_receipts(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);outputs=[]
            for example in ['r3-word.json','r3-continue.json']:
                output=d/(example+'.out')
                subprocess.run([sys.executable,'-m','slc_gen3_r3','run','GEN3_EXECUTE',str(ROOT/'examples'/example),'--state-dir',str(d/'state'),'--output',str(output),'--receipts',str(d/'receipts')],cwd=ROOT,check=True,capture_output=True)
                outputs.append(json.loads(output.read_text()))
            self.assertEqual(outputs[1]['initial'],outputs[0]['states'][-1])
            with open_runtime(state_dir=d/'state') as r:
                self.assertEqual(r.execute('GEN3_STATUS',{})['version'],'SLC-GEN3-R3');self.assertIsNotNone(r.execute('GEN3_CHECKPOINT',{}))
            receipts=list((d/'receipts').glob('*/RECEIPT.json'));self.assertEqual(len(receipts),2)
            for p in receipts:
                row=json.loads(p.read_text());self.assertEqual(row['engine'],'SLC-GEN3-R3');self.assertEqual(row['output_sha256'],hashlib.sha256((p.parent/'OUTPUT.json').read_bytes()).hexdigest())
    def test_deployment_scope_and_actual_memory_evidence(self):
        with open_runtime() as r:
            for op in ['GEN3_REPLICATE','GEN2_TAU_REPLAY','GEN2_SOURCE_BATCH']:
                with self.assertRaises(ValueError):r.execute(op,{})
            self.assertIn('node',r.execute('GEN3_MEMORY_NODE',{'memory':'observations'}))
            with self.assertRaises(ValueError):r.execute('GEN3_MEMORY_APPLY',{'encounter':'unsupplied','observation':1,'evidence':None})
if __name__=='__main__':unittest.main()

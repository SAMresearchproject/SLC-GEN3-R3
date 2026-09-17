"""Admission enforcement tests with explicitly synthetic bookkeeping fixtures."""
import json
from pathlib import Path
import tempfile
import unittest
from GW_COM.runtime.evidence import Store, encode
from GW_COM.runtime.decoder import admission, decode


class DecoderGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        method=self.root/'METHOD.json'
        method.write_bytes(encode({'schema':'GW_COM_METHOD_V1','refs':[],
                                  'scope':'BOOKKEEPING TEST FIXTURE ONLY'}))
        self.store=Store(self.root,self.root/'records',method)
        s=self.store
        raw=s.record('raw','raw_waveform',{'samples':['1','-1']})
        fit=s.record('fit','source_fit',{},parents=[raw])
        residual=s.record('residual','residual_history',{},parents=[raw,fit])
        frame={'sample_spans':[[0,1]],'unit_samples':1,'symbols':['S0']}
        symbols=s.record('symbols','candidate_symbolization',{
            'repetition_groups':[{'bins':[2],'frame_indices':[0,1]}],
            'frames':[frame,frame]},parents=[residual])
        info=s.record('info','information_tests',{'observed_repetition':2,'permutation_p':'1/100'},parents=[symbols,residual])
        self.refs=dict(zip(('raw_waveform','source_fit','residual_history','candidate_symbolization','information_tests'),
                           (raw,fit,residual,symbols,info)))

    def controls(self,physical='PASS',statistical='PASS',name='controls',refs=None):
        return self.store.record(name,'control_results',{
            'physical_controls':[{'name':'fixture','status':physical,'evidence':self.refs['raw_waveform']}],
            'statistical_controls':[{'name':'fixture','status':statistical,'evidence':(refs or self.refs)['information_tests']}]},
            parents=list((refs or self.refs).values()))

    def test_passed_lineage_decodes_with_sample_support(self):
        gate=admission(self.store,'gate',self.refs,self.controls())
        output=decode(self.store,'decoded',gate)
        data=self.store.payload(output)
        self.assertEqual(data['hypotheses'][0]['interval_integers'],[2])
        self.assertEqual(data['hypotheses'][0]['support'][0]['raw_sample_spans'],[[0,1]])

    def test_every_nonpass_status_blocks(self):
        for i,status in enumerate(('NOT_RUN','INCOMPLETE','FAIL')):
            for family in ('physical','statistical'):
                with self.subTest(status=status,family=family):
                    key=family+str(i)
                    controls=self.controls(name='controls'+key,**{family:status})
                    gate=admission(self.store,'gate'+key,self.refs,controls)
                    self.assertFalse(self.store.payload(gate)['eligible'])
                    with self.assertRaises(ValueError):
                        decode(self.store,'decoded'+key,gate)

    def test_empty_controls_do_not_pass(self):
        control=self.store.record('empty','control_results',{
            'physical_controls':[],'statistical_controls':[]},parents=list(self.refs.values()))
        gate=admission(self.store,'gate',self.refs,control)
        self.assertFalse(self.store.payload(gate)['eligible'])

    def test_missing_lineage_is_rejected(self):
        refs=dict(self.refs);refs.pop('source_fit')
        with self.assertRaises(ValueError):
            admission(self.store,'gate',refs,self.controls())

    def test_other_candidate_controls_are_rejected(self):
        refs=dict(self.refs)
        refs['raw_waveform']=self.store.record('otherraw','raw_waveform',{'samples':['2']})
        with self.assertRaises(ValueError):
            admission(self.store,'gate',self.refs,self.controls(refs=refs))

    def test_changed_raw_bytes_invalidate_an_admitted_candidate(self):
        gate=admission(self.store,'gate',self.refs,self.controls())
        path=self.root/self.store.read(self.refs['raw_waveform'])['artifact_refs'][0]['path']
        path.write_text('{"samples":["changed"]}')
        with self.assertRaises(ValueError):
            decode(self.store,'decoded',gate)
        self.assertFalse((self.root/'records/decoded.json').exists())

    def test_summary_status_cannot_override_failed_test_values(self):
        refs=dict(self.refs)
        refs['information_tests']=self.store.record('failedinfo','information_tests',{
            'observed_repetition':1,'permutation_p':'1'},parents=[refs['candidate_symbolization'],refs['residual_history']])
        gate=admission(self.store,'gate',refs,self.controls(refs=refs))
        self.assertFalse(self.store.payload(gate)['eligible'])

    def test_control_status_without_evidence_is_rejected(self):
        control=self.store.record('unsupported','control_results',{
            'physical_controls':[{'status':'PASS'}],
            'statistical_controls':[{'status':'PASS'}]},parents=list(self.refs.values()))
        with self.assertRaises(ValueError):
            admission(self.store,'gate',self.refs,control)

    def test_incomplete_stage_is_rejected(self):
        refs=dict(self.refs)
        refs['information_tests']=self.store.record('unfinished','information_tests',{
            'observed_repetition':2,'permutation_p':'1/100'},
            parents=[refs['candidate_symbolization'],refs['residual_history']],status='INCOMPLETE')
        with self.assertRaises(ValueError):
            admission(self.store,'gate',refs,self.controls(refs=refs))


if __name__=='__main__':unittest.main()

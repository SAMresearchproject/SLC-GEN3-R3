import unittest
from GW_COM.runtime.information import framing,max_repetition


class IntervalLengthTests(unittest.TestCase):
    def markers(self,payload):
        markers=[]
        start=256
        for _ in range(2):
            frame=[start+16*i for i in range(4)]
            for n in payload:frame.append(frame[-1]+16*n)
            markers+=frame;start=frame[-1]+368
        return markers

    def test_seven_values_preserved_including_three(self):
        payload=[2,3,5,7,11,13,17]
        frames=framing(self.markers(payload),7)
        self.assertEqual([f['interval_ratio_bins'] for f in frames],[payload,payload])
        self.assertEqual(max_repetition(frames)[0],2)
        self.assertTrue(all(len(f['sample_spans'])==7 for f in frames))

    def test_historical_six_value_protocol_still_supported(self):
        payload=[2,5,7,11,13,17]
        self.assertEqual([f['interval_ratio_bins'] for f in framing(self.markers(payload))],[payload,payload])

    def test_seven_does_not_accept_truncated_single_frame(self):
        self.assertEqual(framing(self.markers([2,3,5,7,11,13,17])[:10],7),[])


if __name__=='__main__':unittest.main()

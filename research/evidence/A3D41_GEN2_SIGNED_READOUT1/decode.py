"""Decode two source-action changes and one signed N01 current through GEN2.

Usage: python3 decode.py --observations '["first delta", "second delta", 1]'
The action probes are independent, each beginning at the same initial state.
This finite decoder uses the campaign's rho=1 source family.
"""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from SAM_PROJECT.session import DomainSession
HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--observations',required=True,help='JSON array of exact rational action changes followed by the signed N01 readout')
    args=parser.parse_args()
    observed=json.loads(args.observations)
    if not isinstance(observed,list) or len(observed)!=3 or any(type(x) not in (int,str) for x in observed):
        parser.error('Supply three exact integers/rational strings; floats are not accepted.')
    # Canonical scalar normalization is an interface conversion, not a response calculation.
    from fractions import Fraction
    normalized=[]
    for value in observed:
        exact=Fraction(value)
        normalized.append(exact.numerator if exact.denominator==1 else str(exact))
    contract=json.loads((HERE/'DECODER_CONTRACT.json').read_text())
    session=DomainSession(ROOT/'SAM_REVIEW/campaigns/PROJECT_DOMAIN_SESSIONS1/sessions/ATOM3D_c51c939ff7ce489196cfb2aa0bcbfc43')
    try:
        members=session.execute('GEN2_CUSTODY',{'contract':contract,'action':'fiber','visible':normalized},purpose='Decode supplied two-Write-response and signed N01 observations against all 192 retained source configurations.')
        print(json.dumps({'members':members,'member_count':len(members),'rho':1,'observations':normalized,'session':str(session.directory)},indent=2))
    finally:session.close()
if __name__=='__main__':main()

"""Native exact integer services inherited from HFM2's declared grammar."""
from fractions import Fraction
import hashlib

from .exact import ExactError, canonical_bytes, fraction, integer, seal, token

FIELDS = {
    "VECTOR_CURRENT": {"left", "right"},
    "RECEIVER_ACTION": {"left", "right", "current"},
    "EXTERIOR_NEGATION": {"left", "right"},
    "ORIENTATION_APPLY": {"unsigned", "orientation"},
    "FRACTION_AUDIT": {"fraction"},
    "EXACT_FIBER_MEMBER": {"projection_ref", "member_ref", "index", "cardinality"},
    "CANONICAL_BODY": {"body"},
    "DIRECTION_ROW": {"x", "quadratic", "linear", "constant"},
}


def sparse(value):
    if not isinstance(value, dict):
        raise ExactError("sparse history must be a coordinate mapping")
    return {token(key): integer(item) for key,item in sorted(value.items()) if integer(item)}


def combine(left, right, sign=1):
    return {key: value for key in sorted(set(left)|set(right))
            if (value := left.get(key,0)+sign*right.get(key,0))}


def execute(operation, payload):
    if operation not in FIELDS or set(payload) != FIELDS[operation]:
        raise ExactError("inherited exact operation fields differ")
    if operation == "VECTOR_CURRENT":
        left,right = sparse(payload["left"]),sparse(payload["right"])
        even,current = combine(left,right),combine(right,left,-1)
        result = {"even_S":even,"signed_J":current,"recovered_left":left,"recovered_right":right,
                  "inverse_exact":True,"swap_even_invariant":True,"swap_signed_negates":True}
    elif operation == "RECEIVER_ACTION":
        left,right,current = (sparse(payload[key]) for key in ("left","right","current"))
        after_left,after_right = combine(left,current),combine(right,current,-1)
        if any(value < 0 for value in (*after_left.values(),*after_right.values())):
            raise ExactError("receiver action creates negative history custody")
        result = {"left_after":after_left,"right_after":after_right,"inverse_exact":True,
                  "inverse_left":combine(after_left,current,-1),"inverse_right":combine(after_right,current)}
    elif operation == "EXTERIOR_NEGATION":
        left,right = sparse(payload["left"]),sparse(payload["right"])
        if right != {key:-value for key,value in left.items()}:
            raise ExactError("exterior history is not exact directed negation")
        result = {"left":left,"right":right,"expected_right":right,"orientation_reversal_exact":True}
    elif operation == "ORIENTATION_APPLY":
        orientation = integer(payload["orientation"])
        if orientation not in (-1,1):
            raise ExactError("orientation must be exactly -1 or +1")
        result = {"orientation":orientation,
                  "signed":{key:orientation*value for key,value in sparse(payload["unsigned"]).items()}}
    elif operation == "FRACTION_AUDIT":
        value = fraction(payload["fraction"])
        result = {"canonical_fraction":str(value),"numerator_bits":abs(value.numerator).bit_length(),
                  "denominator_bits":value.denominator.bit_length(),"sign":(value>0)-(value<0),
                  "fraction_sha256":hashlib.sha256(str(value).encode()).hexdigest()}
    elif operation == "EXACT_FIBER_MEMBER":
        count,index = integer(payload["cardinality"],minimum=2),integer(payload["index"],minimum=0)
        if index >= count or any(not isinstance(payload[k],dict) or not payload[k]
                                 for k in ("member_ref","projection_ref")):
            raise ExactError("fiber address or source reference differs")
        result = {"member_address":{"cardinality":count,"index":index},
                  "member_ref":payload["member_ref"],"projection_ref":payload["projection_ref"],
                  "reconstructive":True}
    elif operation == "CANONICAL_BODY":
        encoded = canonical_bytes(payload["body"])
        result = {"body_sha256":hashlib.sha256(encoded).hexdigest(),"canonical_bytes":len(encoded)}
    else:
        x,a,b,c = (integer(payload[k]) for k in ("x","quadratic","linear","constant"))
        result = {"value":a*x*x+b*x+c,"arithmetic":"ARBITRARY_WIDTH_EXACT_INTEGER"}
    return seal("Q3_NATIVE_INTEGER_OPERATION_V1",operation=operation,result=result)

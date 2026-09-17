"""Signed subtraction with one-to-one source sample custody."""
from fractions import Fraction as F
from .native import Graph
from .carrier import design


def extract(native, samples, model):
    graph = Graph()
    coeff = [graph.value(v,{'model':model['name'],'coefficient':i}) for i,v in enumerate(model['coefficients'])]
    predictions, residuals = [], []
    for i,y in enumerate(samples):
        predicted = graph.sum([graph.op('MULTIPLY',c,graph.value(x,{'prediction_design_sample':i}))
                               for c,x in zip(coeff,design(i,len(coeff)))])
        predictions.append(predicted)
        residuals.append(graph.op('SUBTRACT',graph.value(y,{'raw_sample':i}),predicted))
    values, receipt = native.evaluate(graph,'GW-COM signed residual: raw minus '+model['name']+' prediction, preserving every sample and alternative')
    prediction = [values[v] for v in predictions]
    residual = [values[v] for v in residuals]
    for i,(p,r) in enumerate(zip(prediction,residual)):
        independent = sum(c*x for c,x in zip(model['coefficients'],design(i,len(coeff))))
        assert p == independent and p+r == samples[i]
    return prediction, residual, receipt

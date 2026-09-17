"""Fit three declared discrete carrier models; retain every alternative."""
from fractions import Fraction as F
from .native import Graph

MODELS = ('C4_amplitude','C4_amplitude_offset','C4_amplitude_offset_drift')


def design(i, size):
    return [F((-1)**i), F(1), F(i,128)*((-1)**i)][:size]


def fit(native, samples, calibration=128):
    graph = Graph()
    y = [graph.value(v, {'calibration_sample':i}) for i,v in enumerate(samples[:calibration])]
    parameters = []
    for size in (1,2,3):
        xs = [design(i,size) for i in range(calibration)]
        # Exact design-matrix constants are compiler inputs; fitted data sums
        # and elimination execute in the native graph.
        matrix = [[graph.value(sum(x[a]*x[b] for x in xs),
                    {'design_gram':[a,b],'model_size':size}) for b in range(size)] for a in range(size)]
        rhs = [graph.sum([graph.op('MULTIPLY',y[i],graph.value(xs[i][j],
                {'design':[i,j],'model_size':size})) for i in range(calibration)]) for j in range(size)]
        for col in range(size):
            pivot = matrix[col][col]
            matrix[col] = [graph.op('DIVIDE',v,pivot) for v in matrix[col]]
            rhs[col] = graph.op('DIVIDE',rhs[col],pivot)
            for row in range(size):
                if row == col:
                    continue
                factor = matrix[row][col]
                matrix[row] = [graph.op('SUBTRACT',a,graph.op('MULTIPLY',factor,b))
                               for a,b in zip(matrix[row],matrix[col])]
                rhs[row] = graph.op('SUBTRACT',rhs[row],graph.op('MULTIPLY',factor,rhs[col]))
        parameters.append(rhs)
    values, receipt = native.evaluate(graph,'GW-COM carrier fitting: calibration-only exact least squares for amplitude, offset and linear amplitude drift; retain all models')
    return [{'name':name,'coefficients':[values[v] for v in ids],
             'calibration_indices':[0,calibration],'holdout_indices':[128,192]}
            for name,ids in zip(MODELS,parameters)], receipt

import numpy as np
try:
    import pandas as pd
except ImportError:
    pass

class Data:
    def __init__(self):
        pass


class DenseData(Data):
    def __init__(self, data, group_names, *args):
        self.groups = args[0] if len(args) > 0 else [np.array([i]) for i in range(len(group_names))]

        l = sum(len(g) for g in self.groups)
        num_samples = data.shape[0]
        t = False
        if l != data.shape[1]:
            t = True
            num_samples = data.shape[1]

        valid = (not t and l == data.shape[1]) or (t and l == data.shape[0])
        assert valid, "# of names must match data matrix!"

        self.weights = args[1] if len(args) > 1 else np.ones(num_samples)
        wl = len(self.weights)
        valid = (not t and wl == data.shape[0]) or (t and wl == data.shape[1])
        assert valid, "# weights must match data matrix!"

        self.transposed = t
        self.group_names = group_names
        self.data = data



def convert_to_data(val):
    if isinstance(val, Data):
        return val
    elif type(val) == np.ndarray:
        return DenseData(val, [str(i) for i in range(val.shape[1])])
    elif str(type(val)) == "<class 'pandas.core.series.Series'>":
        return DenseData(val.as_matrix().reshape((1,len(val))), list(val.index))
    elif str(type(val)) == "<class 'pandas.core.frame.DataFrame'>":
        return DenseData(val.as_matrix(), list(val.columns))
    else:
        assert False, "Unknown type passed as data object: "+str(type(val))

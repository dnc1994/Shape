from rule import Rule

__author__ = 'Linghao Zhang'
__version__ = '0.1.0'

class Inferencer(object):
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self.fsets = {}
        self.rules = []

    def add_rule(self, rule):
        rule = Rule.parse(rule)
        self.rules.append(rule)

    def add_rules(self, rules):
        for rule in rules:
            self.add_rule(rule)

    def add_fset(self, fset):
        self.fsets[fset.name] = fset

    def add_fsets(self, fsets):
        for fset in fsets:
            self.add_fset(fset)

    def get_fset(self, var):
        if not self.fsets.has_key(var):
            return None
        return self.fsets[var]

    def inference(self):
        for rule in self.rules:
            ((var, val), weight) = rule.evaluate(self.inputs, self.fsets)
            if not self.outputs.has_key(var):
                self.outputs[var] = {}
            self.outputs[var][val] = weight

    def fuzzify(self, inputs):
        for var, val in inputs.items():
            print 'fuzzifying: {0} -> {1}'.format(var, val)
            self.inputs[var] = val

    def defuzzify(self):
        results = {}
        for var in self.outputs.keys():
            sort_list = [(v, k) for (k, v) in self.outputs[var].iteritems()]
            print sort_list
            results[var] = sorted(sort_list, reverse=True)[0][1]
        return results

    def evaluate(self, inputs):
        self.fuzzify(inputs)
        self.inference()
        return self.defuzzify()

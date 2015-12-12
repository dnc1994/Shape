import re

__author__ = 'Linghao Zhang'
__version__ = '0.1.0'


class Rule(object):
    operator_mapping = {
        'NONE': lambda x: x[0] if len(x) == 1 else x,
        'AND': min,
        'OR': max,
        'NOT': lambda x: 1 - x
    }

    def __init__(self, antecedent, consequent, operator):
        self._antecedent = antecedent
        self._consequent = consequent
        self._operator = operator

    def evaluate(self, inputs, fsets):
        membership_values = []
        for (var, fset) in self._antecedent:
            # print 'Computing membership: {0}: {1} -> {2}'.format(var, inputs[var], fset)
            negation = False
            if 'NOT' in fset:
                negation = True
                fset = fset.replace('NOT', '').strip()
            membership = fsets[fset].membership(inputs[var])
            membership = membership if not negation else Rule.operator_mapping['NOT'](membership)
            # print 'Membership value: {0}\n'.format(membership)
            membership_values.append(membership)
        weight = Rule.operator_mapping[self._operator](membership_values)
        return self._consequent, weight

    @staticmethod
    def parse(rule):
        if 'AND' in rule:
            operator = 'AND'
        elif 'OR' in rule:
            operator = 'OR'
        else:
            operator = 'NONE'
        antecedent = rule.split('THEN')[0][2:].strip()
        if operator == 'NONE':
            antecedent = [antecedent.split(' IS ')]
        else:
            antecedent = [p.strip().split(' IS ') for p in antecedent.split(operator)]

        consequent = rule.split('THEN')[1].strip().split(' IS ')
        # print antecedent
        # print consequent
        return Rule(antecedent, consequent, operator)


if __name__ == '__main__':
    Rule.parse('IF he IS NOT tall AND she IS short AND she IS heavy THEN marriage IS happy')

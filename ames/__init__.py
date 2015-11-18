"""
ames helper tools
"""

import itertools

def isreal(string):
    try:
        float(string)
    except ValueError:
        return False
    return True

def maybe_value_line(line):
    line_split = line.split()
    return len(line_split) > 1 \
           and all(isreal(x) for x in line_split)

def repair_tabs(inp):
    """
    Replaces tabs with spaces
    """
    if '\t' in inp:
        return inp.replace('\t', ' '), 1
    else:
        return inp, 0

def repair_nlhead(inp):
    """
    Fixes wrong nlhead value
    """
    lines = inp.split('\n')
    nlhead, rest = lines[0].split(None, 1)
    nlhead = int(nlhead)

    potential_nlhead = []
    for i, (a, b) in enumerate(zip(lines, lines[1:]), 1):
        if not maybe_value_line(a) \
                and maybe_value_line(b):
            potential_nlhead.append(i)
    if nlhead != potential_nlhead[-1]:
        # change is required
        nlhead = potential_nlhead[-1]
        lines[0] = '%d %s'%(nlhead, rest)
        return '\n'.join(lines), 10
    else:
        return inp, 0


def repair_bad_nan(inp):
    """
    Fixes wrong nan values
    """
    nan_values = [x.lower() for x in ['--', 'nan', '#WERT!']]
    lines = inp.split('\n')
    nlhead = int(lines[0].split()[0])
    vmiss = lines[11].split()
    badness = [0]
    def correct_nan(line):
        values = line.lower().split()
        for i in xrange(1,len(values)):
            if values[i] in nan_values:
                badness[0] += 1
                values[i] = vmiss[i-1]
        return ' '.join(values)
    header = lines[:nlhead]
    data = [correct_nan(line) for line in lines[nlhead:]]
    return '\n'.join(header + data), badness[0] * 0.1

REPAIR_FUNCTIONS = [
    ('tabs', repair_tabs),
    ('wrong_nlhead', repair_nlhead),
    ('bad_nan', repair_bad_nan),
    ]

class AmesRepairTool(object):
    """
    Repair tool for broken NASA AMES Files
    """
    def repair(self, input_file):
        """
        Loads a broken input file and repairs it.
        """
        inp = input_file.read()

        def apply_repair(repair_functions, inp):
            repaired = []
            for repair_name, repair_function in repair_functions:
                inp, score = repair_function(inp)
                if score > 0:
                    repaired.append(repair_name)
                    print "badness of ", repair_name, ":", score
            return inp, repaired

        results = [apply_repair(functions, inp)
                   for functions
                   in itertools.permutations(REPAIR_FUNCTIONS)]
        results = sorted(results,
                         key=lambda (out, repaired): len(repaired))
        out, repaired = results[0]
        return RepairResult(out, repaired)


class RepairResult(object):
    """
    Represents the result of a repair action.
    """
    def __init__(self, result, badnesses):
        self._result = result
        self._badnesses = badnesses
    @property
    def detected_badnesses(self):
        """
        A list of badnesses detected during the repair.
        """
        return self._badnesses
    def write_to(self, output_file):
        """
        Writes repaired data to given output file.
        """
        output_file.write(self._result)


"""
ames helper tools
"""

class AmesRepairTool(object):
    """
    Repair tool for broken NASA AMES Files
    """
    def repair(self, input_file):
        """
        Loads a broken input file and repairs it.
        """
        return RepairResult(input_file.read(), [])


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


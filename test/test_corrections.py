"""
Test corrections which are applied to ames files
"""
from unittest import TestCase
from ames import AmesRepairTool
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import os

class _CorrectionTestBase(TestCase):
    # pylint: disable=too-many-public-methods
    """
    Base class for tests comparing a function from one file to another.
    """
    testfile = None
    maxDiff = None
    @property
    def reffile(self):
        """
        Reference filename derrived from testfile name
        """
        return self.testfile.replace('.ames', '.corrected.ames')
    @property
    def badness_name(self):
        """
        Name of the tested badness
        """
        _, filename = os.path.split(self.testfile)
        badness, _ = os.path.splitext(filename)
        return badness
    def test_correction_output_matches(self):
        test_out = StringIO()
        repair_tool = AmesRepairTool()
        with open(self.testfile) as inp:
            repaired = repair_tool.repair(inp)
        repaired.write_to(test_out)
        print test_out.getvalue()
        # a second repair pass must return 0 corrections
        test_out.seek(0)
        repaired2 = repair_tool.repair(test_out)
        self.assertEqual(0,
                         len(repaired2.detected_badnesses),
                         "second repair pass yielded a correction")
        with open(self.reffile) as ref:
            self.assertMultiLineEqual(test_out.getvalue(), ref.read())
        self.assertEqual([self.badness_name], repaired.detected_badnesses)

# discover test cases
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(BASEDIR, 'correction_test_cases')
def cases_filter(path):
    return path.endswith('.ames') and 'corrected' not in path
CASES = filter(cases_filter,
               (os.path.join(path, filename)
                for path, _, files in os.walk(DATADIR)
                for filename in files))

def create_cases(cases, target_namespace):
    for case in cases:
        dirname, filename = os.path.split(case)
        _, group = os.path.split(dirname)
        casename, _ = os.path.splitext(filename)
        name = 'Test' + group.upper() + casename.capitalize()
        target_namespace[name] = type(name,
                                      (_CorrectionTestBase,),
                                      {'testfile': case})

create_cases(CASES, locals())

import unittest
import subprocess

from gradescope_utils.autograder_utils.decorators import weight, number

class TestBase(unittest.TestCase): 
    def runStudentCode(self, dirname, name):
        res = subprocess.call(['./run_student_code.sh', dirname])
        if res != 0:
            raise AssertionError(f'Unable to run student\'s Jack Analyzer on {name}.jack!')

    def assertDiffMatch(self, dirname, name):
        res = subprocess.call(['diff', f'/autograder/grader/tests/expected-outputs/{dirname}/{name}.xml', f'/autograder/source/{dirname}/{name}.xml', '--strip-trailing-cr'])
        if res != 0:
            diff = subprocess.check_output(['/bin/sh', '-c', f'diff /autograder/grader/tests/expected-outputs/{dirname}/{name}.xml /autograder/source/{dirname}/{name}.xml --strip-trailing-cr ; exit 0'], text=True)
            print(f'Files differ!\n{diff}')
            raise AssertionError(f'Student\'s XML did not match the provided XML file!')

    def assertCorrectAnalyzer(self, testpath):
        dirname, name = testpath.split('/')
        self.runStudentCode(dirname, name)
        self.assertDiffMatch(dirname, name)
        subprocess.run(['mv', f'/autograder/source/{dirname}/{name}.xml', '/autograder/outputs/'])

class TestModules(TestBase): 
    @weight(47.5/3)
    @number(1)
    def test_square_main(self):
        self.assertCorrectAnalyzer('Square/Main')

    @weight(47.5/3)
    @number(2)
    def test_square_square(self):
        self.assertCorrectAnalyzer('Square/Square')

    @weight(47.5/3)
    @number(3)
    def test_square_square_game(self):
        self.assertCorrectAnalyzer('Square/SquareGame')

    @weight(47.5)
    @number(4)
    def test_array_test_main(self):
        self.assertCorrectAnalyzer('ArrayTest/Main')

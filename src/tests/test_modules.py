import unittest
import subprocess

from gradescope_utils.autograder_utils.decorators import weight, number

class TestBase(unittest.TestCase): 
    def runStudentCode(self, dirname, name):
        res = subprocess.call(['./run_student_code.sh', dirname])
        if res != 0:
            raise AssertionError(f'Unable to run student\'s virtual machine translator on {name}.vm!')

    def assertValidAssembly(self, dirname, name):
        res = subprocess.call(['n2tAssembler', f'/autograder/source/{dirname}/{name}.asm'])
        if res != 0:
            raise AssertionError(f'Unable to assemble student\'s ASM output!')

    def runCPUEmulator(self, dirname, name):
        res = subprocess.call(['n2tCPUEmulator', f'/autograder/source/{dirname}/{name}.tst'])
        if res != 0:
            diff = subprocess.check_output(['diff', f'/autograder/source/{dirname}/{name}.out', f'/autograder/source/{dirname}/{name}.cmp', '-qsw', '--strip-trailing-cr'], stderr=subprocess.STDOUT)
            print(f'Files differ!\n{diff}')
            raise AssertionError(f'Unable to run student\'s ASM on CPU emulator!')

    def assertNoDiff(self, file, expected_file):
        res = subprocess.call(['diff', file, expected_file, '-qsw', '--strip-trailing-cr'])
        if res != 0:
            raise AssertionError(f'Output does not match the expected!')

    def assertCorrectTranslator(self, dirname):
        _, name = dirname.split('/')
        self.runStudentCode(dirname, name)
        self.assertValidAssembly(dirname, name)
        self.runCPUEmulator(dirname, name)
        subprocess.run(['mv', f'/autograder/source/{dirname}/{name}.out', '/autograder/outputs/'])
        self.assertNoDiff(f'/autograder/outputs/{name}.out', f'/autograder/grader/tests/expected-outputs/{dirname}/{name}.cmp')

class TestModules(TestBase): 
    @weight(47.5/4)
    @number(1)
    def test_fibonacci_element(self):
        self.assertCorrectTranslator('FunctionCalls/FibonacciElement')

    @weight(47.5/4)
    @number(2)
    def test_nested_call(self):
        self.assertCorrectTranslator('FunctionCalls/NestedCall')

    @weight(47.5/4)
    @number(3)
    def test_simple_function(self):
        self.assertCorrectTranslator('FunctionCalls/SimpleFunction')

    @weight(47.5/4)
    @number(4)
    def test_statics_test(self):
        self.assertCorrectTranslator('FunctionCalls/StaticsTest')

    @weight(47.5/2)
    @number(5)
    def test_basic_loop(self):
        self.assertCorrectTranslator('ProgramFlow/BasicLoop')

    @weight(47.5/2)
    @number(6)
    def test_fibonacci_series(self):
        self.assertCorrectTranslator('ProgramFlow/FibonacciSeries')

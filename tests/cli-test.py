from unittest import TestCase
from env_backup.command_line import get_parser
import timeout_decorator

from contextlib import redirect_stdout
import io, subprocess, shlex


class TestCommands(TestCase):
    def setUp(self):
        self.parser = get_parser()
        self.f = io.StringIO()
        self.addCleanup(self.f.close)


    @timeout_decorator.timeout(10)
    def test_1_list(self):
        with redirect_stdout(self.f):
            args = self.parser.parse_args(['list'])
            args.func(args)
        self.assertIn('python3', self.f.getvalue())


    @timeout_decorator.timeout(10)
    def test_2_new(self):
        # install a new package
        cmd = subprocess.run(['pip', 'list'], capture_output=True)
        self.assertNotIn('multiprocess', cmd.stdout.decode())

        subprocess.run(['pip', 'install', '--user', 'multiprocess'])
        cmd = subprocess.run(['pip', 'list'], capture_output=True)
        self.assertIn('multiprocess', cmd.stdout.decode())

        with redirect_stdout(self.f):
            args = self.parser.parse_args(['new', '--name', 'test', '-y'])
            args.func(args)
            output_1 = self.f.getvalue()
            self.f.truncate(0)  # clear
            args = self.parser.parse_args(['list'])
            args.func(args)
            output_2 = self.f.getvalue()
            
        self.assertIn('Installed kernelspec python3_test', output_1)
        self.assertIn('python3_test', output_2)
        
        cmd = subprocess.run(['pip', 'list'], capture_output=True)
        self.assertNotIn('multiprocess', cmd.stdout.decode())


    @timeout_decorator.timeout(10)
    def test_3_activate(self):
        cmd = subprocess.run(['pip', 'list'], capture_output=True)
        self.assertNotIn('multiprocess', cmd.stdout.decode())

        command = shlex.split("bash -c 'source env-activate python3_test && env | grep PYTHONUSERBASE'")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        self.assertIn('PYTHONUSERBASE', stdout.decode())
        self.assertIsNone(stderr)

        command = shlex.split("bash -c 'source env-activate python3_test && pip list | grep multiprocess'")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        self.assertIn('multiprocess', stdout.decode())
        self.assertIsNone(stderr)


    @timeout_decorator.timeout(10)
    def test_4_deactivate(self):
        cmd = subprocess.run(['pip', 'list'], capture_output=True)
        self.assertNotIn('multiprocess', cmd.stdout.decode())

        command = shlex.split("bash -c 'source env-activate python3_test && source env-deactivate && env'")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        self.assertIn('PYTHONUSERBASE=\n', stdout.decode())
        self.assertIsNone(stderr)

        command = shlex.split("bash -c 'source env-activate python3_test && source env-deactivate && pip list'")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        self.assertNotIn('multiprocess', stdout.decode())
        self.assertIsNone(stderr)


    @timeout_decorator.timeout(10)
    def test_5_remove(self):
        with redirect_stdout(self.f):
            args = self.parser.parse_args(['remove', 'python3_test'])
            args.func(args)
            output_1 = self.f.getvalue()
            self.f.truncate(0)  # clear
            args = self.parser.parse_args(['list'])
            args.func(args)
            output_2 = self.f.getvalue()

        self.assertIn('Done', output_1)
        self.assertNotIn('python3_test ', output_2)

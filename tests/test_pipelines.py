# -*- coding: utf-8 -*-

"""

test smallparts.pipelines

"""

import subprocess
import unittest

from smallparts import pipelines


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_acstract_pipeline(self):
        """Abstract class"""
        self.assertRaises(
            NotImplementedError,
            pipelines._AbstractPipeline,
            ['ls', '-1d'])

    def test_single_command_pipeline(self):
        """Single command call"""
        ls_call = pipelines.ProcessPipeline(['ls', '-1d'])
        self.assertEqual(
            ls_call.result.stdout,
            b'.\n')
        self.assertRaises(
            pipelines.IllegalStateException,
            ls_call.execute)
        self.assertEqual(
            ls_call.repeat().result.stdout,
            b'.\n')
        self.assertEqual(
            pipelines.ProcessPipeline('ls -1d').result.stdout,
            b'.\n')
        self.assertRaises(
            OSError,
            pipelines.ProcessPipeline,
            ['non-existent-command'])
        self.assertRaisesRegex(
            ValueError,
            '^Invalid command',
            pipelines.ProcessPipeline,
            None)
        self.assertRaisesRegex(
            ValueError,
            '^Please provide at least one command.',
            pipelines.ProcessPipeline)
        self.assertRaises(
            subprocess.TimeoutExpired,
            pipelines.ProcessPipeline,
            'sleep 10',
            timeout=1)
        self.assertRaises(
            subprocess.CalledProcessError,
            pipelines.ProcessPipeline,
            'mkdir .',
            check=True)

    def test_pipeline(self):
        """Shell pipeline call"""
        pipeline_call = pipelines.ProcessPipeline(
            ['ls', '-1d'],
            ['tr', '.', 'x'],
            ['tr', 'x', '-'],
            ['tr', '-', 'u'])
        self.assertEqual(
            pipeline_call.result.stdout,
            b'u\n')
        self.assertWarns(
            UserWarning,
            pipelines.ProcessPipeline,
            ['echo', 'x'],
            ['tr', '-', 'u'],
            input=b'a x b x c')
        self.assertWarns(
            UserWarning,
            pipelines.ProcessPipeline,
            ['echo', 'x'],
            ['tr', '-', 'u'],
            intermediate_stderr=pipelines.PIPE)

    def test_single_command_chain(self):
        """Single command call"""
        ls_call = pipelines.ProcessChain(['ls', '-1d'])
        self.assertEqual(
            ls_call.result.stdout,
            b'.\n')
        self.assertRaises(
            pipelines.IllegalStateException,
            ls_call.execute)
        self.assertEqual(
            ls_call.repeat().result.stdout,
            b'.\n')
        self.assertEqual(
            pipelines.ProcessChain('ls -1d').result.stdout,
            b'.\n')
        self.assertRaises(
            OSError,
            pipelines.ProcessChain,
            ['non-existent-command'])
        self.assertRaisesRegex(
            ValueError,
            '^Invalid command',
            pipelines.ProcessChain,
            None)
        self.assertRaisesRegex(
            ValueError,
            '^Please provide at least one command.',
            pipelines.ProcessChain)

    def test_chain(self):
        """Shell ProcessChain call"""
        pipeline_call = pipelines.ProcessChain(
            ['ls', '-1d'],
            ['tr', '.', 'x'],
            ['tr', 'x', '-'],
            ['tr', '-', 'u'])
        self.assertEqual(
            pipeline_call.result.stdout,
            b'u\n')
        self.assertEqual(
            pipelines.ProcessChain.run(
                ['tr', 'x', '-'],
                ['tr', '-', 'u'],
                input=b'a x b x c').stdout,
            b'a u b u c')


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:

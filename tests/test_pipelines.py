# -*- coding: utf-8 -*-

"""

test smallparts.pipelines

"""

import unittest

from smallparts import pipelines


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_single_command(self):
        """Single command call"""
        ls_call = pipelines.ProcessPipeline(['ls', '-1d'])
        self.assertEqual(
            ls_call.result.stdout,
            b'.\n')
        self.assertRaises(
            pipelines.IllegalStateException,
            ls_call.run)
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


if __name__ == '__main__':
    unittest.main()


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:

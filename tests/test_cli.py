# -*- coding: utf-8 -*-

"""

test smallparts.sequences

"""

import unittest

from smallparts import cli


class TestSimple(unittest.TestCase):

    """Test the module"""

    def test_single_command(self):
        """Single command call"""
        ls_call = cli.ProcessPipeline(['ls', '-1d'])
        self.assertEqual(
            ls_call.result.stdout,
            b'.\n')
        self.assertRaises(
            cli.IllegalStateException,
            ls_call.run)
        self.assertEqual(
            ls_call.repeat().result.stdout,
            b'.\n')
        self.assertEqual(
            cli.ProcessPipeline('ls -1d').result.stdout,
            b'.\n')
        self.assertRaises(
            OSError,
            cli.ProcessPipeline,
            ['non-existent-command'])
        self.assertRaisesRegex(
            ValueError,
            '^Invalid command',
            cli.ProcessPipeline,
            None)
        self.assertRaisesRegex(
            ValueError,
            '^Please provide at least one command.',
            cli.ProcessPipeline)

    def test_pipeline(self):
        """Shell pipeline call"""
        pipeline_call = cli.ProcessPipeline(
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

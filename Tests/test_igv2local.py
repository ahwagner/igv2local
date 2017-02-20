from unittest import TestCase
from igv2local import process_arguments, Session
import filecmp
import os
import shutil


class TestProcessArguments(TestCase):
    def test_help(self):
        args = ['-h']
        with self.assertRaises(SystemExit) as cm:
            process_arguments(args)
        self.assertEqual(cm.exception.code, 0)

    def test_str_args(self):
        args = ['--out', '/test/dir', 'my.xml']
        parsed = process_arguments(args)
        self.assertEquals(parsed.out, '/test/dir')
        self.assertEquals(parsed.xml_file, 'my.xml')


class TestSession(TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir('test_output')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('test_output')

    def setUp(self):
        self.s = Session('test.xml', 'test_output')

    def test_parse_xml(self):
        self.s.parse_xml()
        self.assertEquals(self.s.xml_tree.getroot().tag, 'Session')

    def test_write_xml(self):
        self.s.write_xml()
        self.assertTrue(filecmp.cmp('test.xml', 'test_output/test.xml'))

    def test_copy_files_to_local(self):
        # test for file copy
        self.s.copy_files_to_local()
        self.assertTrue(os.path.isfile('test_output/test.bam'))
        self.assertTrue(os.path.isfile('test_output/test.bam.bai'))
        # test for corresponding change to xml
        files = [x.get('path') for x in self.s.xml_tree.getroot().find('Resources')]
        self.assertListEqual(files, ['test_output/test.bam'])

    def test_create_local(self):
        self.fail()

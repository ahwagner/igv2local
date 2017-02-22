from unittest import TestCase
from igv2local.igv2local import main, Session
from definitions import ROOT_DIR
import os
import shutil


class TestMain(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('test_dir')

    def test_help(self):
        args = ['-h']
        with self.assertRaises(SystemExit) as cm:
            main(args)
        self.assertEqual(cm.exception.code, 0)

    def test_main(self):
        xml = '/'.join([ROOT_DIR, 'Tests', 'test.xml'])
        args = ['--out', 'test_dir', xml]
        self.assertFalse(os.path.exists('test_dir'))
        with self.assertRaises(SystemExit) as cm:
            main(args)
        self.assertEqual(cm.exception.code, 0)
        self.assertTrue(os.path.exists('test_dir'))
        self.assertTrue(os.path.isfile('test_dir/test.xml'))
        self.assertTrue(os.path.isfile('test_dir/test.bam'))
        self.assertTrue(os.path.isfile('test_dir/test.bam.bai'))


def trees_equal(t1, t2):
    return elements_equal(t1.getroot(), t2.getroot())


def elements_equal(e1, e2):
    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False
    # Note: all([]) returns True
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))


class TestSession(TestCase):

    @classmethod
    def setUpClass(cls):
        os.mkdir('test_output')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('test_output')
        os.unlink('web_test.xml')

    def setUp(self):
        xml = '/'.join([ROOT_DIR, 'Tests', 'test.xml'])
        self.s = Session(xml, 'test_output')

    def test_parse_xml(self):
        self.s.parse_xml()
        self.assertEqual(self.s.xml_tree.getroot().tag, 'Session')

    def test_write_xml(self):
        self.s.parse_xml()
        self.s.write_xml()
        new_session = Session('test_output/test.xml', 'test_output')
        new_session.parse_xml()
        self.assertTrue(trees_equal(new_session.xml_tree, self.s.xml_tree))

    def test_copy_files_to_local(self):
        # test for file copy
        self.s.copy_files_to_local()
        self.assertTrue(os.path.isfile('test_output/test.bam'))
        self.assertTrue(os.path.isfile('test_output/test.bam.bai'))
        # test for corresponding change to xml
        resource_files = [x.get('path') for x in self.s.xml_tree.getroot().find('Resources')]
        track_set = set()
        for panel in self.s.xml_tree.getroot().findall('Panel'):
            for track in panel.findall('Track'):
                track_set.add(track.get('id'))
        self.assertListEqual(resource_files, ['test_output/test.bam'])
        self.assertSetEqual(track_set, {'test_output/test.bam', 'test_output/test.bam_coverage'})

    def test_create_local(self):
        self.s.create_local()
        self.assertTrue(os.path.isfile('test_output/test.bam'))
        self.assertTrue(os.path.isfile('test_output/test.bam.bai'))
        self.assertTrue(os.path.isfile('test_output/test.xml'))

        xml = '/'.join([ROOT_DIR, 'Tests', 'test.xml'])
        new_session = Session(xml, 'test_output')
        new_session.parse_xml()
        self.assertFalse(trees_equal(self.s.xml_tree, new_session.xml_tree))

    def test_parse_web_xml(self):
        web_xml = "https://gscweb.gsc.wustl.edu/gscmnt/gc2547/griffithlab/awagner/web_test.xml"
        new_session = Session(web_xml)
        self.assertEqual(str(new_session.igv_xml_file), 'web_test.xml')
        self.assertTrue(os.path.isfile('web_test.xml'))

    def test_auto_generate_output_dir(self):
        xml = '/'.join([ROOT_DIR, 'Tests', 'foobar.xml'])
        new_session = Session(xml)
        self.assertEqual(new_session.output_directory, 'foobar')

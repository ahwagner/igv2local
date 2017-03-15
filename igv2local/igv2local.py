import argparse
from gmstk.linusbox import LinusBox
import xml.etree.ElementTree as ET
import re
from pathlib import Path
import sys

"""igv2local

Import XML document defining an IGV session and recreate all needed files
locally.
"""


class Session:

    linus = LinusBox()
    linus.connect()

    def __init__(self, igv_xml_file, output_directory=None):
        if re.match(r'^https?://', igv_xml_file):
            remote_path = self._url_to_path(igv_xml_file)
            print('Downloading remote .xml file...')
            self.linus.ftp_get(str(remote_path), remote_path.name)
            self.igv_xml_file = Path(remote_path.name)
        else:
            self.igv_xml_file = Path(igv_xml_file)
        if output_directory is not None:
            self.output_directory = Path(output_directory)
        else:
            self.output_directory = Path(self.igv_xml_file.stem)
        self.xml_tree = None
        self.report_status = False
        self.ignore_existing = False

    def parse_xml(self):
        if self.report_status:
            print('Parsing session .xml...')
        self.xml_tree = ET.parse(self.igv_xml_file)

    def write_xml(self):
        if self.report_status:
            print('Writing session to local .xml...')
        self.xml_tree.write(self.output_directory / self.igv_xml_file.name)

    @staticmethod
    def _url_to_path(url):
        return Path(re.sub(r'https://gscweb.gsc.wustl.edu', '', url))

    def copy_files_to_local(self):
        path_dict = dict()
        if self.xml_tree is None:
            self.parse_xml()
        root = self.xml_tree.getroot()
        for resource in root.find('Resources'):
            web_path = resource.get('path')
            path = self._url_to_path(web_path)
            local_path = self.output_directory / path.name
            path_dict[web_path] = str(local_path)
            if self.report_status:
                print("copying remote to {}...".format(local_path))
            if self.ignore_existing and local_path.is_file():
                print("skipping (file {} already exists)".format(str(local_path)))
            else:
                self.linus.ftp_get(str(path), str(local_path))
            if local_path.suffix == '.bam':
                if self.report_status:
                    print("copying remote to {}...".format(local_path) + '.bai')
                if self.ignore_existing and local_path.with_suffix('.bam.bai').is_file():
                    print("skipping (file {} already exists)".format(str(local_path)))
                else:
                    self.linus.ftp_get(str(path) + '.bai', str(local_path) + '.bai')
            resource.set('path', str(local_path))
        for panel in root.findall('Panel'):
            for track in panel.findall('Track'):
                track_id = track.get('id')
                if track_id.endswith('_coverage'):
                    path = path_dict[track_id[:-9]] + '_coverage'
                elif not path_dict.get(track_id):
                    continue
                else:
                    path = path_dict[track_id]
                track.set('id', path)

    def create_local(self, report_status=None, ignore_existing=None):
        if report_status is not None:
            self.report_status = report_status
        if ignore_existing is not None:
            self.ignore_existing = ignore_existing
        self.parse_xml()
        self.copy_files_to_local()
        self.write_xml()


def main(args=None):
    parser = argparse.ArgumentParser(description='Import XML document defining an IGV session and recreate all needed files locally.')
    parser.add_argument('xml_file', metavar='xml', type=str, help='Remote IGV session file')
    parser.add_argument('--out', type=str, help='output directory (default cwd)')
    parser.add_argument('--ignore-existing', action='store_true', help='do not overwrite or compare local files with remote')
    if args is None:
        parsed = parser.parse_args()
    else:
        parsed = parser.parse_args(args)
    s = Session(parsed.xml_file, parsed.out)
    s.create_local(report_status=True, ignore_existing=parsed.ignore_existing)
    sys.exit(0)


if __name__ == '__main__':
    main()

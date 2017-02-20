import argparse
from gmstk.linusbox import LinusBox
import xml.etree.ElementTree as ET
import re
from pathlib import Path

"""igv2local

Import XML document defining an IGV session and recreate all needed files
locally.
"""

# Track = namedtuple('Track', ['Session', 'Resources', 'Panels', 'PanelLayout',
#                              'HiddenAttributes'])
#
# Panel


class Session:

    linus = LinusBox()
    linus.connect()

    def __init__(self, igv_xml_file, output_directory):
        self.igv_xml_file = igv_xml_file
        self.output_directory = Path(output_directory)
        self.xml_tree = None

    def parse_xml(self):
        self.xml_tree = ET.parse(self.igv_xml_file)

    def write_xml(self):
        self.xml_tree.write()

    def copy_files_to_local(self):
        if self.xml_tree is None:
            self.parse_xml()
        root = self.xml_tree.getroot()
        for resource in root.find('Resources'):
            web_path = resource.get('path')
            path = Path(re.sub(r'https://gscweb.gsc.wustl.edu', '', web_path))
            # resource.set('path', path)
            local_path = self.output_directory / path.name
            self.linus.ftp_get(str(path), str(local_path))
            if local_path.suffix == '.bam':
                self.linus.ftp_get(str(path), str(local_path) + '.bai')
            resource.set('path', str(local_path))

    def create_local(self):
        pass


def process_arguments(args=None):
    parser = argparse.ArgumentParser(description='Import XML document defining an IGV session and recreate all needed files locally.')
    parser.add_argument('xml_file', metavar='xml', type=str, help='Remote IGV session file')
    parser.add_argument('--out', default='.', type=str, help='output directory (default cwd)')
    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)

if __name__ == '__main__':
    args = process_arguments()
    s = Session(args.xml_file, args.out)

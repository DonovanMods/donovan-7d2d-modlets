import fnmatch
import os
# import xml.etree.ElementTree as ET

from glob import glob
from pathlib import Path
from colorama import Fore, Style
from lxml import etree


# Read in XML configs
def readConfigs(path):
    XML = etree.Element('root')

    with os.scandir(path) as configs:
        for config in configs:
            filename = Path(config)
            if config.is_file() and filename.suffix == '.xml':
                XML.append(etree.parse(str(filename)).getroot())

    return XML


def readModlets(configs):
    for modlet_dir in glob('*/Config'):
        passfail = True
        print(
            f'{Fore.YELLOW}Checking {os.path.dirname(Path(modlet_dir))}:{Style.RESET_ALL}', end='')

        with os.scandir(Path(modlet_dir)) as modlets:
            for modlet in modlets:
                filename = Path(modlet)
                if modlet.is_file() and filename.suffix == '.xml':
                    for line in etree.parse(str(filename)).getroot():
                        if 'xpath' in line.attrib:
                            xpath = './' + line.attrib['xpath']
                            # print('XPATH is', xpath)
                            if len(configs.xpath(xpath)) == 0:
                                passfail = False
                                print(
                                    f'\n{Fore.RED}FAIL: {Style.RESET_ALL}{filename} on line:')
                                print(line.values()[0])
        if passfail:
            print(f'{Fore.GREEN} OKAY {Style.RESET_ALL}')


configXML = readConfigs(
    Path('S:/Games/Steam/steamapps/common/7 Days To Die/Data/Config'))
readModlets(configXML)

# TODO: Write the combined XML out to a file (should be an option)
# etree.ElementTree(configXML).write('test.xml')

# print(configXML.xpath(
# "./blocks/block[starts-with(@name, 'garageDoorMetal')]/property[@name='OnlySimpleRotations']/@value")[0])

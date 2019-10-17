import sys

from os import scandir
from pathlib import Path
from shutil import copy

from colorama import Fore, Style
from lxml import etree


def colortext(color, message):
    return f'{color}{message}{Style.RESET_ALL}'


def cleanAIO(path):
    directory = path

    for clean_me in directory.glob('*'):
        print('\t', colortext(Fore.RED, clean_me))
        if clean_me.is_dir():
            cleanAIO(clean_me)
            try:
                Path.rmdir(clean_me)
            except RuntimeError as error:
                print(
                    f'Unable to remove directory {clean_me}: {colortext(Fore.RED, error)}')
                sys.exit(1)
        else:
            try:
                Path.unlink(clean_me)
            except RuntimeError as error:
                print(
                    f'Unable to remove file {clean_me}: {colortext(Fore.RED, error)}')
                sys.exit(1)


def readXML(path, dir=None, xmlfiles={}):
    XMLparser = etree.XMLParser(ns_clean=True, remove_blank_text=True)

    if not dir:
        dir = path

    for configfile in path.glob('*'):
        if configfile.is_dir():
            readXML(configfile, path, xmlfiles)
            continue

        key = configfile.relative_to(dir)

        if configfile.suffix == '.xml':

            if key not in xmlfiles:
                xmlfiles[key] = etree.Element('configs')

            xmlfiles[key].append(etree.Comment(
                f' Included from {configfile.parts[0]} '))

            for node in etree.parse(str(configfile), XMLparser).getroot():
                xmlfiles[key].append(node)

        else:
            xmlfiles[key] = configfile

    return xmlfiles


def writeXML(aio_mod, xmlfiles):
    for key in xmlfiles:
        aio_file = Path(aio_mod, 'config', key)
        value = xmlfiles[key]

        print('\t', colortext(Fore.GREEN, aio_file))

        if not aio_file.parent.exists():
            Path.mkdir(aio_file.parent)

        if aio_file.suffix == '.xml':
            try:
                etree.ElementTree(value).write(
                    str(aio_file), pretty_print=True)
            except RuntimeError as error:
                print(
                    f'Unable to write XML file {value}: {colortext(Fore.RED, error)}')
                sys.exit(1)
        else:
            copy(value, aio_file)


##
# Main()
##
aio_mod = 'donovan-aio'
included_mods = [
    'donovan-betterbandages',
    'donovan-betterbridges',
    'donovan-betterbuffs',
    'donovan-betterpowertools',
    'donovan-bettervehicles',
    'donovan-bigbackpack',
    'donovan-lessgrind',
    'donovan-longerlootbags',
    'donovan-megastacks',
    'donovan-moreperks',
]

# Clean AIO files
print(colortext(Fore.RED, f'Cleaning'))
cleanAIO(Path(aio_mod, 'config'))

# Read files
xmls = {}
print(colortext(Fore.YELLOW, f'Reading'))
for mod in included_mods:
    print('\t', colortext(Fore.YELLOW, mod))
    xmls.update(readXML(Path(mod, 'config')))

# Write files
print(colortext(Fore.GREEN, f'Writing'))
writeXML(aio_mod, xmls)

sys.exit(0)

#!env python3
import sys

from os import scandir
from pathlib import Path

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

        if configfile.name == 'localization.txt':
            if key not in xmlfiles:
                xmlfiles[key] = []

            with configfile.open() as lf:
                next(lf)
                xmlfiles[key] += lf.readlines()

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

        if aio_file.name == 'localization.txt':
            if not aio_file.is_file():
                with aio_file.open("w") as lf:
                    lf.write('Key,Source,Context,Changes,English\n')

            # ... do stuff
            with aio_file.open("a") as lf:
                lf.writelines(value)


##
# Main()
##
modlistFile = Path(Path(sys.argv[0]).parent, 'modlist.txt')
includedMods = []
aio_mod = 'donovan-aio'

if modlistFile.exists:
    with open(modlistFile) as f:
        includedMods = list(f)
else:
    print(f'Unable to open {modlistFile.name}')
    sys.exit(1)

# Clean AIO files
print(colortext(Fore.RED, f'Cleaning'))
cleanAIO(Path(aio_mod, 'config'))

# Read files
xmls = {}
print(colortext(Fore.YELLOW, f'Reading'))
for mod in includedMods:
    modFile = mod.strip()
    modConfig = Path(modFile, 'config')

    if modConfig.exists:
        print('\t', colortext(Fore.YELLOW, modFile))
        xmls.update(readXML(modConfig))
    else:
        print(f"{modFile} doesn't appear to be a modlet")


# Write files
print(colortext(Fore.GREEN, f'Writing'))
writeXML(aio_mod, xmls)

sys.exit(0)

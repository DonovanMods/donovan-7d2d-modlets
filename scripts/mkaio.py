from os import scandir
from pathlib import Path

from colorama import Fore, Style
from lxml import etree

xmlfiles = {}
included_mods = [
    'donovan-betterbandages',
    'donovan-betterbridges',
    'donovan-betterbuffs',
    'donovan-betterpowertools',
    'donovan-bettervehicles',
    'donovan-lessgrind',
    'donovan-longerlootbags',
    'donovan-megastacks',
    'donovan-moreperks',
]


def colortext(color, message):
    return f'{color}{message}{Style.RESET_ALL}'


XMLparser = etree.XMLParser(ns_clean=True, remove_blank_text=True)

print(colortext(Fore.YELLOW, f'Reading'))

for mod in included_mods:
    print('\t', colortext(Fore.YELLOW, mod))

    for xmlfile in Path(mod).glob('**/config/*.xml'):
        xmlkey = xmlfile.stem

        if xmlkey not in xmlfiles:
            xmlfiles[xmlkey] = etree.Element('configs')

        xmlfiles[xmlkey].append(etree.Comment(
            f' Included from {xmlfile.parts[0]} '))

        for node in etree.parse(str(xmlfile), XMLparser).getroot():
            xmlfiles[xmlkey].append(node)


print(colortext(Fore.GREEN, f'Writing'))

for config in xmlfiles:
    xmlfile = f'donovan-aio/config/{config}.xml'
    xml = xmlfiles[config]

    print('\t', colortext(Fore.GREEN, xmlfile))
    etree.ElementTree(xml).write(xmlfile, pretty_print=True)

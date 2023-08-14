#!env python3
import sys
import getopt

from os import scandir
from pathlib import Path

from colorama import Fore, Style
from lxml import etree


def colortext(color, message):
    return f'{color}{message}{Style.RESET_ALL}'


def cleanBundle(path):
    directory = path

    for clean_me in directory.glob('*'):
        if options['verbose']:
            print('\t', colortext(Fore.WHITE, clean_me))

        if clean_me.is_dir():
            cleanBundle(clean_me)
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
        filetype = None

        if configfile.is_dir():
            readXML(configfile, path, xmlfiles)
            continue

        if options['debug']:
            print(f"\t\tReading data from '{configfile.name}'", end=': ')

        key = configfile.relative_to(dir)

        if configfile.suffix.lower() == '.xml':
            filetype = "XML"

            if key not in xmlfiles:
                xmlfiles[key] = etree.Element('bundle')

            xmlfiles[key].append(etree.Comment(
                f' Included from {configfile.parts[2]} '))

            for node in etree.parse(str(configfile), XMLparser).getroot():
                xmlfiles[key].append(node)

        if configfile.name.lower() == 'localization.txt':
            filetype = "LOCALIZATION"

            if key not in xmlfiles:
                xmlfiles[key] = []

            with configfile.open() as lf:
                next(lf)
                xmlfiles[key] += lf.readlines()

        if options['debug']:
            print(filetype or 'UNKNOWN')

    return xmlfiles


def writeXML(bundle, xmlfiles):
    if not bundle.is_dir():
        Path.mkdir(bundle)

    for key in xmlfiles:
        bundle_file = bundle / 'Config' / key
        value = xmlfiles[key]

        if options['verbose']:
            print('\t', colortext(Fore.WHITE, bundle_file))

        if not bundle_file.parent.exists():
            Path.mkdir(bundle_file.parent)

        if bundle_file.suffix.lower() == '.xml':
            try:
                etree.ElementTree(value).write(
                    str(bundle_file), pretty_print=True)
            except RuntimeError as error:
                print(
                    f'Unable to write XML file {value}: {colortext(Fore.RED, error)}')
                sys.exit(1)

        if bundle_file.name.lower() == 'localization.txt':
            if not bundle_file.is_file():
                with bundle_file.open("w") as lf:
                    lf.write('Key,Source,Context,Changes,English\n')

            with bundle_file.open("a") as lf:
                lf.writelines(value)


def getoptions():
    def help():
        def format(command, description):
            return f'\t{command:20} - {description}'

        print(f'Usage: {Path(sys.argv[0]).name} [opts]')
        print('\nOpts:')
        print(
            f'{format("-b|--bundle <name>", "The name of the bundled modlet to create")}')
        print(f'{format("-m|--modlets <file>", "a file containing a list of the modlets to bundle, one per line")}')
        print()
        print(
            f'{format("-C|--clean", "Clean the previous bundled directory before writing")}')
        print(f'{format("-v|--verbose", "display more output during run")}')
        print(f'{format("-h|--help", "this help message")}')
        sys.exit(2)

    options = {
        'bundle': Path('./bundle'),
        'modlets': Path(Path(sys.argv[0]).parent, 'modlist.txt'),
        'clean': False,
        'debug': False,
        'verbose': False,
    }

    short_args = 'b:Chm:v'
    long_args = ['bundle', 'clean', 'debug', 'help', 'modlets', 'verbose']

    try:
        arguments, values = getopt.getopt(sys.argv[1:], short_args, long_args)
    except getopt.error as err:
        print(str(err))
        sys.exit(1)

    for arg, value in arguments:
        if arg in ('-m', '--modlets'):
            if Path(value).exists():
                options['modlets'] = Path(value)
            else:
                print(colortext(
                    Fore.RED, f"\nE: Could not find or read from the modlets file '{value}'\n"))
                help()

        if arg in ('-b', '--bundle'):
            options['bundle'] = Path(value)

        if arg in ('-C', '--clean'):
            options['clean'] = True

        if arg in ('-v', '--verbose'):
            options['verbose'] = True

        if arg in ('-h', '--help'):
            help()

        if arg in ('--debug'):
            options['debug'] = True

    if options['modlets'] == None:
        help()

    if options['bundle'] == None:
        print(colortext(Fore.RED, 'E: No bundle name was provided'))
        help()

    return options


##
# Main()
##
includedMods = []

options = getoptions()
modlistFile = options['modlets']
bundle = options['bundle']

if modlistFile.exists:
    with open(modlistFile) as f:
        includedMods = list(f)
else:
    print(f'Unable to open {modlistFile.name}')
    sys.exit(1)

# Read files
xmls = {}
if options['verbose']:
    print(colortext(Fore.GREEN, f'\nReading'))

for mod in includedMods:
    modFile = mod.strip()
    modConfig = Path(modFile, 'Config')

    if modConfig.exists():
        if options['verbose']:
            print('\t', colortext(Fore.WHITE, modFile))
        xmls.update(readXML(modConfig))
    else:
        print(
            colortext(Fore.YELLOW, f"\t! {modFile} doesn't appear to be a modlet"))


if not any(xmls):
    print(colortext(Fore.RED, '\nNo XML data was generated, please check your inputs\n'))
    sys.exit(1)

# Clean bundled files
if options['clean']:
    if options['verbose']:
        print(colortext(Fore.GREEN, f'\nCleaning'))

    cleanBundle(Path(bundle, 'Config'))

# Write files
if options['verbose']:
    print(colortext(Fore.GREEN, f'\nWriting to {bundle.name}'))

writeXML(bundle, xmls)

sys.exit(0)

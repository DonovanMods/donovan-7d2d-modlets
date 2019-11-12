#!env python3
import sys
import getopt

from os import scandir
from pathlib import Path

from colorama import Fore, Style
from lxml import etree


def colortext(color, message):
    return f'{color}{message}{Style.RESET_ALL}'


def cleanAIO(path):
    directory = path

    for clean_me in directory.glob('*'):
        if options['verbose']:
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
    if not aio_mod.is_dir():
        Path.mkdir(aio_mod)

    for key in xmlfiles:
        aio_file = aio_mod / 'Config' / key
        value = xmlfiles[key]

        if options['verbose']:
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

            with aio_file.open("a") as lf:
                lf.writelines(value)


def getoptions():
    def help():
        def format(command, description):
            return f'\t{command:20} - {description}'

        print(
            f'Usage: {Path(sys.argv[0]).name} -c [config_file] -m [bundled_modlet_name]')
        print('\nOpts:')
        print(f'{format("-c|--config <file>", "a file containing a list of the modlets to bundle, one per line")}')
        print(
            f'{format("-m|--modlet <name>", "The name of the bundled modlet to create")}')
        print()
        print(f'{format("-v|--verbose", "display more output during run")}')
        print(f'{format("-h|--help", "this help message")}')
        sys.exit(2)

    options = {
        'config': Path(Path(sys.argv[0]).parent, 'modlist.txt'),
        'modlet': Path('./bundle'),
        'debug': False,
        'verbose': False,
    }

    short_args = 'c:hm:v'
    long_args = ['config', 'debug', 'help', 'modlets', 'verbose']

    try:
        arguments, values = getopt.getopt(sys.argv[1:], short_args, long_args)
    except getopt.error as err:
        print(str(err))
        sys.exit(1)

    for arg, value in arguments:
        if arg in ('-c', '--config'):
            if Path(value).exists():
                options['config'] = Path(value)
            else:
                print(colortext(
                    Fore.RED, f"\nERROR: Could not find or read from the config file '{value}'\n"))
                help()

        if arg in ('-m', '--modlet'):
            options['modlet'] = Path(value)

        if arg in ('--debug'):
            options['debug'] = True

        if arg in ('-h', '--help'):
            help()

        if arg in ('-v', '--verbose'):
            options['verbose'] = True

    if options['config'] == None:
        help()

    if options['modlet'] == None:
        print(colortext(Fore.RED, 'ERROR: No modlet name was provided'))
        help()

    return options


##
# Main()
##
includedMods = []

options = getoptions()
modlistFile = options['config']
aio_mod = options['modlet']

if modlistFile.exists:
    with open(modlistFile) as f:
        includedMods = list(f)
else:
    print(f'Unable to open {modlistFile.name}')
    sys.exit(1)

# Clean AIO files
if options['verbose']:
    print(colortext(Fore.RED, f'Cleaning'))

cleanAIO(Path(aio_mod, 'Config'))

# Read files
xmls = {}
if options['verbose']:
    print(colortext(Fore.YELLOW, f'Reading'))

for mod in includedMods:
    modFile = mod.strip()
    modConfig = Path(modFile, 'Config')

    if modConfig.exists:
        if options['verbose']:
            print('\t', colortext(Fore.YELLOW, modFile))
        xmls.update(readXML(modConfig))
    else:
        print(colortext(Fore.YELLOW,
                        f"{modFile} doesn't appear to be a modlet"))


# Write files
if options['verbose']:
    print(colortext(Fore.GREEN, f'Writing'))

writeXML(aio_mod, xmls)

sys.exit(0)

import getopt
import sys
from copy import copy
from glob import glob
from os import scandir
from pathlib import Path

from colorama import Fore, Style
from lxml import etree


# returns a message in the given color
def colortext(color, message):
    return f'{color}{message}{Style.RESET_ALL}'


# Flattens and returns the given array
def flatten(array):
    return [item for items in array for item in items]


# Read all config XML files into one massive XML (this is what 7 days does internally)
def readConfigs(path):
    XML = etree.Element('root')

    with scandir(path) as configs:
        for config in configs:
            filename = Path(config)

            if config.is_file() and filename.suffix == '.xml':
                XML.append(etree.parse(str(filename)).getroot())

    return XML


# Read and validate our modlet XML files
def readModlets(original_configs):
    for modlet_dir in options['modlets']:
        if not modlet_dir.exists() or not modlet_dir.is_dir():
            continue

        # don't clobber other modlets while validating
        configs = copy(original_configs)

        passfail = True
        base_filename = Path(modlet_dir).parent
        parser = etree.XMLParser(ns_clean=True, remove_comments=True)
        stats['modlets'] += 1

        if options['verbose']:
            if options['debug']:
                print('\n')

            print(f'{colortext(Fore.YELLOW, base_filename):40}\t', end='')

        with scandir(Path(modlet_dir)) as modlets:

            for modlet in modlets:
                filename = Path(modlet)

                if modlet.is_file() and filename.suffix == '.xml':
                    stats['modfiles'] += 1

                    for line in etree.parse(str(filename), parser).getroot():
                        if 'xpath' in line.attrib:
                            xpath = line.attrib['xpath']
                            new_value = line.text
                            tag = line.tag
                            attrib = None
                            if tag in ['set', 'removeattribute']:
                                attrib = xpath.split('@')[-1]
                            if tag == 'setattribute':
                                attrib = line.attrib['name']

                            # add a / to the beginning of xpath if it's not already there
                            if xpath[0] != '/':
                                xpath = f'/{xpath}'

                            # add a . to the beginning of xpath for search purposes
                            xpath = f'.{xpath}'

                            results = configs.xpath(xpath)

                            if options['debug']:
                                print('\nFILE:', base_filename)
                                print('TAG:', tag)
                                print('XPATH:', xpath)
                                print('RESULTS:', results)
                                print('ATTRIB:', attrib)
                                print('NEW VALUE:', new_value)

                            if results:
                                for result in results:
                                    if tag in ['set', 'setattribute']:
                                        if attrib:
                                            result.getparent().set(attrib, new_value)
                                        continue

                                    if tag == 'removeattribute':
                                        if attrib:
                                            result.getparent().removeattribute(attrib)
                                        continue

                                    if tag == 'append':
                                        for child in line:
                                            result.append(child)
                                        continue

                                    if tag == 'remove':
                                        result.getparent().remove(result)
                                        continue

                                    break
                            else:
                                stats['failures'] += 1
                                passfail = False
                                print(
                                    f'\n{colortext(Fore.RED, "FAIL: ")}{filename} on line {line.sourceline}:\n{line.values()[0]}')

        if passfail and options['verbose']:
            print(f'{colortext(Fore.GREEN, "OKAY")}')


def getoptions():
    def help():
        def format(command, description):
            return f'\t{command:20} - {description}'

        print(f'Usage: {Path(sys.argv[0]).name} -c <directory> [opts]')
        print('\nOpts:')
        print(f'{format("-c|--config <dir>", "the game XML config directory")}')
        print(f'{format("-m|--modlets <dir>", "where we should look for modlets (can be repeated) -- Default is current directory")}')
        print(f'\n{format("-v|--verbose", "display successes as well as failures during run -- failures always show")}')
        print(
            f'\n{format("-d|--debug", "produces copious amounts of output, not recommended for normal use!")}')
        print(f'\n{format("-h|--help", "this help message")}')
        sys.exit(2)

    options = {
        'config': None,
        'debug': False,
        'modlets': [],
        'verbose': False,
    }

    short_args = 'c:dhm:v'
    long_args = ['config', 'debug', 'help', 'modlets', 'verbose']

    try:
        arguments, values = getopt.getopt(sys.argv[1:], short_args, long_args)
    except getopt.error as err:
        print(str(err))
        sys.exit(1)

    for arg, value in arguments:
        if arg in ('-c', '--config'):
            options['config'] = value

        if arg in ('-m', '--modlets'):
            modlets = flatten([Path(value).glob('**/Config')])

            if modlets:
                options['modlets'].append(modlets)
            else:
                print(f'{value!r} is not a valid modlet directory -- skipping')

        if arg in ('-d', '--debug'):
            options['debug'] = True

        if arg in ('-h', '--help'):
            help()

        if arg in ('-v', '--verbose'):
            options['verbose'] = True

    # Flatten the modlets list
    options['modlets'] = [item for items in options['modlets']
                          for item in items]

    if options['config'] == None:
        print('You must provide a directory for us to validate against -- generally this should be the 7 days Data/Config directory')
        help()

    if not options['modlets']:
        if options['verbose']:
            print('No modlets provided on command line, using current directory\n')

        options['modlets'] = Path('.').glob('**/Config')

    if not Path(options['config']).exists():
        print(f'{options["config"]!r} is not a valid directory')
        sys.exit(1)

    return options


def print_stats(stats):
    if stats['failures']:
        print(colortext(Fore.RED,
                        f'\nFound {stats["failures"]} failures in {stats["modfiles"]} XML files across {stats["modlets"]} modlets'))
    else:
        print(colortext(Fore.GREEN,
                        f'\nAll {stats["modlets"]} modlets are OKAY'))


##
# Main()
##
stats = {
    'failures': 0,
    'modfiles': 0,
    'modlets': 0,
}
options = getoptions()

if options['debug']:
    print(options)

configXML = readConfigs(options['config'])
readModlets(configXML)

if options['verbose']:
    print_stats(stats)

if options['debug']:
    etree.ElementTree(configXML).write('debug.xml')

import getopt
import sys
from copy import copy
from glob import glob
from os import scandir
from pathlib import Path

from colorama import Fore, Style
from lxml import etree


def colortext(color, message):
    return f'{color}{message}{Style.RESET_ALL}'

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
    for modlet_dir in glob('*/Config'):
        # don't clobber other modlets while validating
        configs = copy(original_configs)
        passfail = True
        base_filename = Path(modlet_dir).parent
        parser = etree.XMLParser(ns_clean=True, remove_comments=True)

        if options['verbose']:
            print(f'{colortext(Fore.YELLOW, base_filename):50}', end='')

        with scandir(Path(modlet_dir)) as modlets:

            for modlet in modlets:
                filename = Path(modlet)

                if modlet.is_file() and filename.suffix == '.xml':
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
                                if attrib:
                                    for result in results:
                                        if tag in ['set', 'setattribute']:
                                            result.getparent().set(attrib, new_value)
                                            continue

                                        if tag == 'removeattribute':
                                            result.getparent().removeattribute(attrib)
                                            continue

                                        break
                            else:
                                passfail = False
                                print(
                                    f'\n{colortext(Fore.RED, "FAIL: ")}{filename} on line {line.sourceline}:\n{line.values()[0]}')

        if passfail and options['verbose']:
            print(f'{colortext(Fore.GREEN, "OKAY")}')


def help():
    print(
        f'Usage: {Path(sys.argv[0]).name} -c <directory> [opts]\n\nOpts:')
    print('\t-c|--config <directory>: the game XML config directory')
    print('\t-m|--modlets <directory>: where we should look for modlets')
    print('\n\t-h|--help: this help message')
    print('\t-v|--verbose: display successes as well as failures during run -- failures always show')
    print('\n\t-d|--debug: produces copious amounts of output, not recommended for normal use!')
    sys.exit(2)


options = {
    'config': None,
    'debug': False,
    'modlets': ['.'],
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

    if arg in ('-d', '--debug'):
        options['debug'] = True

    if arg in ('-h', '--help'):
        help()

    if arg in ('-v', '--verbose'):
        options['verbose'] = True

if options['config'] == None:
    print('You must provide a directory for us to validate against -- generally this should be the 7 days Data/Config directory')
    help()

if not Path(options['config']).exists():
    print(f'{options["config"]!r} is not a valid directory')
    sys.exit(1)

configXML = readConfigs(options['config'])
readModlets(configXML)

if options['debug']:
    etree.ElementTree(configXML).write('debug.xml')

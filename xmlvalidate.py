import getopt
import os
import sys
from copy import copy
from glob import glob
from pathlib import Path
from colorama import Fore, Style
from lxml import etree


# Read all config XML files into one massive XML (this is what 7 days does internally)
def readConfigs(path):
    XML = etree.Element('root')

    with os.scandir(path) as configs:
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

        if options['verbose']:
            print(f'{Fore.YELLOW}Checking {base_filename}:{Style.RESET_ALL}', end='')

        with os.scandir(Path(modlet_dir)) as modlets:

            for modlet in modlets:
                filename = Path(modlet)

                if modlet.is_file() and filename.suffix == '.xml':
                    for line in etree.parse(str(filename)).getroot():

                        # As of now, we can only validate the `set` commands
                        if line.tag == 'set' and 'xpath' in line.attrib:
                            xpath = line.attrib['xpath']
                            new_value = line.text
                            attrib = xpath.split('@')[-1]

                            # add a / to the beginning of xpath if it's not already there
                            if xpath[0] != '/':
                                xpath = f'/{xpath}'

                            # add a . to the beginning of xpath for search purposes
                            xpath = f'.{xpath}'

                            results = configs.xpath(xpath)

                            if options['debug']:
                                print('\nFILE:', base_filename)
                                print('XPATH:', xpath)
                                print('RESULTS:', results)
                                print('ATTRIB:', attrib)
                                print('NEW VALUE:', new_value)

                            if results:
                                for result in results:
                                    result.getparent().set(attrib, new_value)
                            else:
                                passfail = False
                                print(
                                    f'\n{Fore.RED}FAIL: {Style.RESET_ALL}{filename} on recipe:\n{line.values()[0]}')

        if passfail and options['verbose']:
            print(f'{Fore.GREEN} OKAY {Style.RESET_ALL}')


def help():
    print(
        f'Usage: {Path(sys.argv[0]).name} -c <directory> [opts]\n\nOpts:')
    print('\t-c|--config <directory>: the game config directory we should use')
    print('\t-h|--help: this help message')
    print('\t-v|--verbose: display successes as well as failures during run -- failures always show')
    print('\n\t-d|--debug: produces copious amounts of output, not recommended for normal use!')
    sys.exit(2)


options = {
    'config': None,
    'debug': False,
    'verbose': False,
}

short_args = 'c:dhv'
long_args = ['config', 'debug', 'help', 'verbose']

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
    print(f'"{options["config"]}" is not a valid directory')
    sys.exit(1)

configXML = readConfigs(options['config'])
readModlets(configXML)

if options['debug']:
    etree.ElementTree(configXML).write('debug.xml')

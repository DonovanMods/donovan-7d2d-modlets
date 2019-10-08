import getopt
import os
import sys
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
        if options['verbose']:
            print(
                f'{Fore.YELLOW}Checking {os.path.dirname(Path(modlet_dir))}:{Style.RESET_ALL}', end='')

        with os.scandir(Path(modlet_dir)) as modlets:
            for modlet in modlets:
                filename = Path(modlet)
                if modlet.is_file() and filename.suffix == '.xml':
                    for line in etree.parse(str(filename)).getroot():
                        if 'xpath' in line.attrib:
                            xpath = './' + line.attrib['xpath']
                            result = configs.xpath(xpath)
                            if options['debug']:
                                print('\nFILE:', os.path.dirname(
                                    Path(modlet_dir)))
                                print('XPATH:', xpath)
                                print('RESULT:', result)
                            if len(result) == 0:
                                passfail = False
                                print(
                                    f'\n{Fore.RED}FAIL: {Style.RESET_ALL}{filename} on recipe:\n{line.values()[0]}')

        if passfail and options['verbose']:
            print(f'{Fore.GREEN} OKAY {Style.RESET_ALL}')


def help():
    print('Usage: validate -c <directory> [opts]\n\nOpts:')
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

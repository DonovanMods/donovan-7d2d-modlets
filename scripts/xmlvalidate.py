#!/usr/bin/env python3
"""Validate modlet XPath patches against the game's XML config files.

Each file under a modlet's Config/ directory is matched to the game config
file at the same relative path (subdirectories such as XUi_InGame/ included),
and every xpath attribute is evaluated against that file. An xpath that
matches nothing would produce a "WRN XML patch ... did not apply" in-game,
so it is reported as a failure here.

Requires: python-lxml
"""

import getopt
import sys
from pathlib import Path

from lxml import etree

COLOR = sys.stdout.isatty()


def colortext(color, message):
    codes = {'red': '31', 'green': '32', 'yellow': '33', 'white': '37'}
    if not COLOR:
        return message
    return f'\033[{codes[color]}m{message}\033[0m'


# ops that carry an xpath attribute in the game's XPath DSL
XPATH_OPS = {'set', 'setattribute', 'append', 'prepend', 'insertAfter',
             'insertBefore', 'remove', 'removeattribute', 'csv', 'conditional'}

game_cache = {}


def game_tree(config_dir, relpath):
    """Parse (and cache) the game config file for a modlet-relative path."""
    if relpath not in game_cache:
        gamefile = config_dir / relpath
        if gamefile.is_file():
            parser = etree.XMLParser(recover=True, huge_tree=True)
            game_cache[relpath] = etree.parse(str(gamefile), parser)
        else:
            game_cache[relpath] = None
    return game_cache[relpath]


def validate_modlet(modlet_dir, config_dir, options, stats):
    failures = []
    modlet_config = modlet_dir / 'Config'
    stats['modlets'] += 1

    for modfile in sorted(modlet_config.rglob('*.xml')):
        stats['modfiles'] += 1
        relpath = modfile.relative_to(modlet_config)

        try:
            modtree = etree.parse(str(modfile))
        except etree.XMLSyntaxError as error:
            failures.append(f'{modfile}: XML syntax error: {error}')
            continue

        gametree = game_tree(config_dir, relpath)
        if gametree is None:
            failures.append(f'{modfile}: no matching game file {str(relpath)!r}')
            continue

        for node in modtree.iter():
            if not isinstance(node.tag, str) or node.tag not in XPATH_OPS:
                continue
            xpath = node.get('xpath')
            if xpath is None:
                continue

            # the game DSL allows xpaths without a leading slash
            query = xpath if xpath.startswith('/') else f'//{xpath}'

            if options['debug']:
                print(f'\nFILE: {modfile}\nTAG: {node.tag}\nXPATH: {xpath}')

            try:
                results = gametree.xpath(query)
            except etree.XPathEvalError as error:
                failures.append(
                    f'{modfile}:{node.sourceline}: invalid xpath {xpath!r} ({error})')
                continue

            matched = len(results) if isinstance(results, list) else 1
            if not matched:
                failures.append(
                    f'{modfile}:{node.sourceline}: no match for {xpath!r}')

    if options['verbose'] or failures:
        print(f'{colortext("yellow", str(modlet_dir)):50}\t', end='')
        print(colortext('green', 'OKAY') if not failures else colortext('red', 'FAIL'))

    for failure in failures:
        print(f'  {colortext("red", "FAIL:")} {failure}')

    stats['failures'] += len(failures)


def find_modlets(path):
    """Every directory under path (or path itself) holding a ModInfo.xml + Config/."""
    return sorted(p.parent for p in Path(path).glob('**/ModInfo.xml')
                  if (p.parent / 'Config').is_dir())


def getoptions():
    def help():
        print(f'Usage: {Path(sys.argv[0]).name} -c <directory> [opts] ')
        print('\nOpts:')
        print('\t-c|--config <dir>  - the game XML config directory')
        print('\t-m|--modlets <dir> - where to look for modlets (repeatable, default: ./modlets)')
        print('\t-v|--verbose       - display successes as well as failures')
        print('\t-d|--debug         - copious output, not for normal use')
        print('\t-h|--help          - this help message')
        sys.exit(2)

    options = {'config': None, 'debug': False, 'modlets': [], 'verbose': False}

    try:
        arguments, _ = getopt.getopt(
            sys.argv[1:], 'c:dhm:v',
            ['config=', 'debug', 'help', 'modlets=', 'verbose'])
    except getopt.error as err:
        print(str(err))
        sys.exit(1)

    for arg, value in arguments:
        if arg in ('-c', '--config'):
            options['config'] = Path(value)
        elif arg in ('-m', '--modlets'):
            found = find_modlets(value)
            if found:
                options['modlets'] += found
            else:
                print(f'{value!r} contains no modlets -- skipping')
        elif arg in ('-d', '--debug'):
            options['debug'] = True
        elif arg in ('-v', '--verbose'):
            options['verbose'] = True
        elif arg in ('-h', '--help'):
            help()

    if options['config'] is None or not options['config'].is_dir():
        print('You must provide the game Data/Config directory to validate against')
        help()

    if not options['modlets']:
        options['modlets'] = find_modlets('modlets')

    return options


##
# Main()
##
stats = {'failures': 0, 'modfiles': 0, 'modlets': 0}
options = getoptions()

for modlet in options['modlets']:
    validate_modlet(modlet, options['config'], options, stats)

if stats['failures']:
    print(colortext(
        'red',
        f'\nFound {stats["failures"]} failures in {stats["modfiles"]} XML files across {stats["modlets"]} modlets'))
else:
    print(colortext('green', f'\nAll {stats["modlets"]} modlets are OKAY'))

sys.exit(1 if stats['failures'] else 0)

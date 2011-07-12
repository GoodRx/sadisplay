# -*- coding: utf-8 -*-
"""
Program for generating plantuml or dot format
of a database tables by connection string

\n\nDatabase connection string - http://goo.gl/3GpnE
"""
import operator
import string
from optparse import OptionParser
from sqlalchemy import create_engine, MetaData
from sadisplay import describe, render, __version__


def run():
    """Command for reflection database objects"""
    parser = OptionParser(version=__version__,
        description=__doc__)

    parser.add_option('-u', '--url', dest='url',
                    help='Database URL (connection string)')

    parser.add_option('-r', '--render', dest='render', default='dot',
                    choices=['plantuml', 'dot'],
                    help='Output format - plantuml or dot')

    parser.add_option('-l', '--list', dest='list', action='store_true',
                    help='Output database list of tables and exit')

    parser.add_option('-i', '--include', dest='include',
                    help='List of tables to include through ","')

    parser.add_option('-e', '--exclude', dest='exclude',
                    help='List of tables to exlude through ","')

    (options, args) = parser.parse_args()

    if not options.url:
        print '-u/--url option required'
        exit(1)

    engine = create_engine(options.url, pool_size=5, max_overflow=0)
    meta = MetaData()

    meta.reflect(bind=engine)

    if options.list:
        print 'Database tables:'
        tables = sorted(meta.tables.keys())

        for i in xrange(0, len(tables), 2):
            print '  %s' % tables[i:i + 1][0] \
                + ' ' * (38 - len(tables[i:i + 1][0])) \
                + tables[i + 1:i + 2][0]

        exit(0)

    tables = set(meta.tables.keys())

    if options.include:
        tables &= set(map(string.strip, options.include.split(',')))

    if options.exclude:
        tables -= set(map(string.strip, options.exclude.split(',')))

    desc = describe(map(lambda x: operator.getitem(meta.tables, x), tables))
    print getattr(render, options.render)(desc)

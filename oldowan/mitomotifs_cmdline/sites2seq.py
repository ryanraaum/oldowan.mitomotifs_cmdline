import os
import sys
import csv

from optparse import OptionParser

from oldowan.mitomotifs import sites2seq
from oldowan.fasta import entry2str

def run_command():
    """Transform human mtDNA sequence to variable sites."""

    # Set up the options parser
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option('-r',
                      '--region',
                      dest='region',
                      default='hvr1',
                      help='which predefined sequence region to generate (default hvr1)'
                           '(one of hvr1, hvr2, hvr1to2, coding, or all)')
    parser.add_option('-b',
                      '--begin',
                      dest='begin',
                      type='int',
                      default=None,
                      help='define a region to generate (use with --end)')
    parser.add_option('-e',
                      '--end',
                      dest='end',
                      type='int',
                      default=None,
                      help='define a region to generate (use with --begin)')

    # Parse the options
    (options, args) = parser.parse_args()

    # The filename is always required
    if len(args) != 1:
        print 'You must provide a filename!'
        print "Type 'sites2seq -h' for help."
        sys.exit(1)

    # make sure the sites file exists
    if not os.path.exists(args[0]):
        print 'ERROR: Could not find file: %s' % args[0]
        sys.exit(1)

    count = 0
    for entry in csv.reader(open(args[0], 'rU')):
        count += 1
        if len(entry) != 3:
            print 'ERROR: Problem on row %d of the input file' % count
            sys.exit(1)
        name = entry[0]
        n = int(entry[1])
        sites = entry[2]

        region = options.region
        if options.begin is not None and options.end is not None:
            if options.end < options.begin:
                # wrap through the origin
                region = range(options.begin, 16570)+range(1, options.end+1)
            else:
                region = range(options.begin, options.end+1)
        sequence = sites2seq(sites, region=region)

        entry = {'name':name, 'sequence':sequence}
        for i in range(n):
            print entry2str(entry)



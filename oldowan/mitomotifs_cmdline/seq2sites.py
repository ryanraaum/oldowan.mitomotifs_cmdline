import os
import sys

from optparse import OptionParser

from oldowan.mitomotifs import seq2sites
from oldowan.mitomotifs import sites2str
from oldowan.fasta import fasta

def run_command():
    """Transform human mtDNA sequence to variable sites."""

    # Set up the options parser
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option('-a',
                      '--ambig-cutoff',
                      dest='ambig_cutoff',
                      type='int',
                      default=10,
                      help='how many ambiguous sites are acceptable')
    parser.add_option('-w',
                      '--word-size',
                      dest='word_size',
                      type='int',
                      default=15,
                      help='word size in alignment (not generally changed)')
    parser.add_option('-m',
                      '--mismatch-cutoff',
                      dest='mismatch_cutoff',
                      type='float',
                      default=0.7,
                      help='mismatch cutoff for alignment (not generally changed)')

    # Parse the options
    (options, args) = parser.parse_args()

    # The filename is always required
    if len(args) != 1:
        print 'You must provide a filename!'
        print "Type 'seq2sites -h' for help."
        sys.exit(1)

    # make sure the sequence FASTA file exists
    if not os.path.exists(args[0]):
        print 'ERROR: Could not find file: %s' % args[0]
        sys.exit(1)

    for entry in fasta(args[0], 'r'):
        sites = seq2sites(entry['sequence'], 
                          word_size = options.word_size,
                          mismatch_cutoff = options.mismatch_cutoff,
                          ambig_cutoff = options.ambig_cutoff)
        print '"%s","%s"' % (entry['name'], sites2str(sites))


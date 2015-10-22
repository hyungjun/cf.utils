#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : nearest_idx.py
# CREATED BY : hjkim @IIS.2015-10-23 06:24:16.112065
# MODIFED BY :
#
# USAGE      : $ ./nearest_idx.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser


def nearest_idx(aSrc,val):
    '''
    aSrc    : 1d-array
    val     : a value or values in 1d-array to search
    return nearest index
    '''

    if hasattr(val,'__iter__'):
        return [abs(aSrc-v).argmin() for v in val]

    else:
        return abs(aSrc-val).argmin()


def main(args,opts):
    print args
    print opts

    return


if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

#    parser.add_option('-r','--rescan',action='store_true',dest='rescan',
#                      help='rescan all directory to find missing file')

    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print_help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)



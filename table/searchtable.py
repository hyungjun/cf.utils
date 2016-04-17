#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : searchtable.py
# CREATED BY : hjkim @IIS.2015-10-17 08:20:29.873525
# MODIFED BY :
#
# USAGE      : $ ./tablesearch.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    numpy           import array, ma, arange, resize
import  operator


def searchtable( aSrc, cols, values, funcs='=', ret_all=False ):
    '''
    aSrc    : source numpy 2d-array
    cols    : indices of target columns which start with 0
    values  : data to be matched or None (get an entire column)

    func    : ['=', '>', '<', '!=', ..., '~']
              '~' for fuzzy searching

    ret_all : return only selected columns or all columns


    e.g.)
    searchtable( aSrc, (0, 3, 2), ('test', 3000, None), ('~','>', None) )
    '''

    funcComp    = { '=': operator.ne, '!=': operator.eq,
                    '>': operator.lt, '<' : operator.gt}


    if not hasattr(cols,    '__iter__') : cols      = [ cols ]
    if not hasattr(values,  '__iter__') : values    = [ values ]
    if not hasattr(funcs,   '__iter__') : funcs     = [ funcs ]

    Mask    = []


    for col, val, fn in map( None, cols, values, funcs ):

        aCol    = aSrc[:, col]

        '''
        try:
            blank   = aCol.astype('S1') == ' '

        except:
            print '\n\t!! Warning... : error occured (ignored) converting unicode to ascii !!\n'
            blank   = array( [s.encode('ascii', 'ignore') for s in aCol.tolist()] ).astype('S1') == ' '
        '''
        if fn in funcComp:
            mask    = funcComp[ fn ]( aCol, [val]*aCol.size )

        elif fn == '~':
            mask    = [val not in s for s in aCol]

        else:
            raise KeyError, '%s is not supported operator.'%func

        #print mask

        Mask.append(  mask )
        #Mask.append( blank | mask )


    Mask        = array( Mask ).any(0)

    idxRow      = ma.array( arange( aSrc.shape[0] ), mask=Mask ).compressed()

    aOut        = aSrc[ idxRow ]

    if ret_all == True:
        return aOut

    else:
        return aOut[:, cols]


def main(args,opts):
    print args
    print opts

    from numpy import load

    srcPath     = '/data1/hjkim/git/coreFrame/io/GRDC/20150527_GRDC_Stations.npy'

    aSrc        = load(srcPath)
    keys        = aSrc[0].tolist()

    river       = searchtable(aSrc[1:],
                              [keys.index('station'),keys.index('d_yrs')],
                              ['OBIDO',50],
                              ['~','>'], ret_all=True)
    print river

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



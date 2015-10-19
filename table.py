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

from    numpy           import array, ma, arange
from    searchtable     import searchtable
import  operator


class Table( object ):

    def __init__(self, aSrc, cols=None, axis_col=0):
        self.set_table( aSrc, cols, axis_col )


    def set_table( self, aSrc, cols=None, axis_col=0):

        self._table_    = aSrc
        self._table_ori_= aSrc.copy()

        self.cols       = map(int, range(aSrc.shape[1])) if cols==None  \
                     else cols

        self.axis_col   = axis_col
        self.filters    = {}


    def __getitem__(self, slc):
        return self._table_[slc]

    def sorted( self, key, reverse=True ):

        slc         = slice(None, None, -1) if reverse else \
                      slice(None, None, None)

        iCol        = self.cols.index(key)
        self._table_= self._table_[ self._table_[:, iCol].argsort() ][slc]


    def filtered(self, key, value, fnComp):
        '''
        * for sequential filetering

        e.g., grdc.filtered('m_yrs', 100, '>').filtered('area',10000, '>').filtered('river','amazon','~')
        '''

        table       = self.search( key, value, fnComp, ret_all=True )

        if table.size == 0:
            raise ValueError, 'all records filtered out! [] returned!'

        else:
            self.filters[ key ]     = [value, fnComp]
            self._table_            = table

        return self


    @property
    def rows(self):
        return self._table_[:, self.axis_col ].tolist()


    def reset_table(self):
        self.filters    = {}
        self._table_    = self._table_ori_
        self.rows       = self._table_[:, self.axis_col].tolist()


    def search( self, cols, values, funcs='=', ret_all=False ):
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

        cols    = [self.cols.index( col ) for col in cols] if hasattr( cols, '__iter__') \
             else self.cols.index( cols )

        return searchtable( self._table_, cols, values, funcs, ret_all )


def main(args,opts):
    print args
    print opts

    from numpy import *

    srcPath     = '/data1/hjkim/git/coreFrame/io/GRDC/20150527_GRDC_Stations.npy'

    aSrc        = load(srcPath)
    keys        = aSrc[0].tolist()

    river       = Table( aSrc[1:] )
    print river.search(
                              [keys.index('station'),keys.index('d_yrs')],
                              ['OBIDO',50],
                              ['~','>'], ret_all=True)
    '''
    river       = searchtable(aSrc[1:],
                              [keys.index('station'),keys.index('d_yrs')],
                              ['OBIDO',50],
                              ['~','>'], ret_all=True)
    '''
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



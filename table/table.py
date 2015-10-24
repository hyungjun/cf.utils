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

from    numpy                       import array, ma, arange
from    searchtable                 import searchtable
from    cf.utils.ordereddict        import OrderedDict
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


    def __getitem__(self, Slc):
        '''
        river[::2,     ['grdc_no','lat','long']]
        river[1201500, ['grdc_no','lat','long']]
        '''

        Slc = [Slc, slice(None,None,None)] if not hasattr( Slc, '__iter__' ) else Slc

        slc_r, slc_c    = Slc


        if type( slc_r ) != slice           :
            if not hasattr( slc_r, '__iter__' ) :   slc_r = [slc_r]
            slc_r = [ self.rows.index( slc ) for slc in slc_r ]

        print self.cols
        if type( slc_c ) != slice           :
            if not hasattr( slc_c, '__iter__' ) :   slc_c = [slc_c]
            slc_c = [ self.cols.index( slc ) for slc in slc_c ]

        table   = self._table_[slc_r, slc_c]

        return self.post_getitem( table )


    def post_getitem(self, value):
        return value


    def __len__(self):
        return len( self.rows )


    def __iter__(self):
        return self


    def next(self):

        if not hasattr(self, 'curr'):
            self.curr = -1

        if self.curr >= len(self)-1:

            self.curr   = -1
            raise StopIteration

        else:
            self.curr +=1

            return OrderedDict( zip( self.cols, self._table_[ self.curr ]) )


    def sorted( self, key, reverse=True ):

        slc         = slice(None, None, -1) if reverse else \
                      slice(None, None, None)

        iCol        = self.cols.index(key)
        self._table_= self._table_[ self._table_[:, iCol].argsort() ][slc]


    def select(self, keys, values, fnComps):
        '''
        * for sequential filetering

        e.g., grdc.filtered('m_yrs', 100, '>').filtered('area',10000, '>').filtered('river','amazon','~')
        '''

        #table       = self.search( keys, values, fnComps, ret_all=True )
        cols    = [self.cols.index( k ) for k in keys] if hasattr( keys, '__iter__') \
             else self.cols.index( keys )

        table       = searchtable( self._table_, cols, values, fnComps, True )

        if table.size == 0:
            raise ValueError, 'all records filtered out! [] returned!'

        else:
            self.filters[ keys ]     = [values, fnComps]
            self._table_            = table

        return self


    @property
    def rows(self):
        return self._table_[:, self.axis_col ].tolist()


    def reset_table(self):
        self.filters    = {}
        self._table_    = self._table_ori_
        self.rows       = self._table_[:, self.axis_col].tolist()


    def search( self, keys, values, funcs='=', ret_raw=False, ret_all=True ):
        '''
        aSrc    : source numpy 2d-array
        keys    : keys of target columns in self.cols
        values  : data to be matched or None (get an entire column)

        func    : ['=', '>', '<', '!=', ..., '~']
                  '~' for fuzzy searching

        ret     : ['table',     #
                   'array',     #
                   ]

        ret_raw : True          # numpy array for all colums
                  False         # Table instance

        ret_all : True          # return all columns
                  False         # return only selected columns

        e.g.)
        searchtable( aSrc, (0, 3, 2), ('test', 3000, None), ('~','>', None) )
        '''

        cols    = [self.cols.index( key ) for key in keys] if hasattr( keys, '__iter__') \
             else self.cols.index( key )

        table   = searchtable( self._table_, cols, values, funcs, ret_all )

        if ret_raw:
            return table

        else:
            cols    = self.cols if ret_all else [ self.cols[i] for i in cols ]
            return self.new_instance( table, cols )
            #return type(self)( table, cols )
            #return self.__class__(table, cols)


    def new_instance(self, table, cols):
        return self.__class__( table, cols )


def main(args,opts):
    print args
    print opts

    from numpy import load

    srcPath     = '/data1/hjkim/git/coreFrame/io/GRDC/20150527_GRDC_Stations.npy'

    aSrc        = load(srcPath)
    keys        = aSrc[0].tolist()

    river       = Table( aSrc[1:], cols=keys )

    print river[::2, ['grdc_no','lat','long']]
    print river[1201500, ['grdc_no','lat','long']]


    riv         = river.search(
                              ['station','d_yrs'],
                              ['OBIDO',50],
                              ['~','>'], ret_all=False)

    for r in riv: print r
    '''
    river       = searchtable(aSrc[1:],
                              [keys.index('station'),keys.index('d_yrs')],
                              ['OBIDO',50],
                              ['~','>'], ret_all=True)
    '''

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



#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : cached.py
# CREATED BY : hjkim @IIS.2015-12-11 20:18:07.598840
# MODIFED BY :
#
# USAGE      : $ ./cached.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys,types

from    cStringIO       import StringIO
import  lz4

from    numpy           import load, save, array


class Cached( object ):
    '''
    mode    in ['cached', 'update', 'skip', False]

    name    : name of cached files i
              type is <type 'str'>, function
              first arg will be the name of function called followed by args

    dir     : directory to store cached file

    compress: compress option in ['lz4', False]

    verbose : print details to screen
    '''

    mode    = 'cached'
    verbose = True

    def __init__(self, dir, name=None, mode=None, verbose=None, compress='lz4'):

        self.dir        = dir
        self.compress   = compress

        if name != None:
            self.name   = name
        else:
            self.name   = lambda fnName, A: '%s_%s'%(fnName, '.'.join( map(str,A) ))

        if mode != None:
            self.mode   = mode

        if verbose != None:
            self.verbose= verbose


    def __call__(self, func):

        def wrapper( *args, **kwargs):

            if 'CACHED' in kwargs:
                Option  = kwargs.pop( 'CACHED' )
                for k,v in Option.items():
                    self.__dict__[ k ]   = v

            for k,v in kwargs.items():
                if k.startswith('CACHED_'):
                    self.__dict__[ k.split('_')[1].lower() ] = v


            if self.mode in [False, 'skip']:
                return func( *args, **kwargs )


            if type(self.name) != str:
                name = self.name( func.__name__, args )

            else:
                name = self.name

            if not os.path.exists(self.dir)      :   os.makedirs(self.dir)

            cachePath   = os.path.join(self.dir, name)

            if self.compress not in [False, None]:
                cachePath   = cachePath + '.%s'%self.compress

            if os.path.exists( cachePath ) and self.mode != 'update':
                if self.compress != 'lz4':
                    cached  = open(cachePath,'r')
                else:
                    cached  = StringIO( lz4.loads( open(cachePath,'r').read() ) )

                if self.verbose: print '\t!! Cached from %s'%cachePath
                return load( cached )

            else:
                aOut    = func( *args, **kwargs )

                if self.compress=='lz4':
                    cached  = StringIO()
                    save( cached, aOut )
                    open(cachePath,'w').write( lz4.dumps( cached.getvalue() ) )

                else:
                    save( open(cachePath,'w'), aOut )

                if self.verbose: print '\t!! Cached to %s'%cachePath
                return aOut

        return wrapper


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



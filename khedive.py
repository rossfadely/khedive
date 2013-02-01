import os
import numpy as np
import ctypes as ct

# TO-DO: - add more kernels
#        - add FFT tricks
#        - automatic bandwidth estimation

class KDE(object):
    """
    KDE in multi-dimensions.
    """
    def __init__(self,samples=None,bandwidths=None,
                 KDEtypes=None, dll_path='./_khedive.so'):

        self.dll_path = dll_path
        self._define_KDE_function()

        self.samples = samples
        self.KDEtypes = KDEtypes
        self.bandwidths = bandwidths

        if samples==None:
            print '\nNo samples given, running demo'
            self.run_demo()
        else:
            self.run_estimator()

    def run_demo(self):

        s = np.random.randn(1000,1)
        s[:500] = s[:500] * 0.5 + 0.3
        self.samples = np.sort(s,axis=0)

        self.KDEtypes = 'triangular'
        self.bandwidths = 0.3
        self.run_estimator()

        fig = pl.figure()
        pl.hist(self.samples,40,alpha=0.2,normed=True)
        pl.plot(self.samples,self.pdf,'r',lw=2,label=self.KDEtypes)
        pl.show()
        print '\nEnter filename to save figure, or return to exit'
        name = raw_input()
        if len(name)!=0:
            fig.savefig(name)


        s = np.random.randn(2000,2)
        s[:500,0] = s[:500,0] * 0.5 + 0.3
        s[:500,1] = s[:500,1] * 0.3 + 0.5
        s[500:,0] = s[500:,0] - 1.0
        s[500:,1] = s[500:,1] - 0.5
        self.samples = s

        self.KDEtypes = 'triangular'
        self.bandwidths = 0.3
        self.run_estimator()

        fig = pl.figure()
        pl.plot(self.samples[:,0],self.samples[:,1],'ok',
                alpha=0.2,label=self.KDEtypes)
        pl.show()

    def run_estimator(self):

        # declarations
        Nsamp = np.int64(self.samples.shape[0])
        Ndim  = np.int64(self.samples.shape[1])
        self.pdf = np.zeros(self.samples.shape[0]).astype('float64')

        # prep
        self.check_bandwidths()        
        KDEtypes = self.get_KDEtypes()
        KDEtypes_p = KDEtypes.ctypes.data_as(ct.POINTER(ct.c_longlong))
        bandwidths_p = self.bandwidths.ctypes.data_as(ct.POINTER(ct.c_double))
        samples_p = self.samples.ctypes.data_as(ct.POINTER(ct.c_double))
        pdf_p = self.pdf.ctypes.data_as(ct.POINTER(ct.c_double))

        # kde
        self.estimator(Nsamp,Ndim,KDEtypes_p,
                       bandwidths_p,samples_p,pdf_p)


    def check_bandwidths(self):
        """
        check bandwidths in correct format,
        automatic bw not supported yet
        """
        if isinstance(self.bandwidths,float):
            self.bandwidths = np.array(self.bandwidths)
            self.bandwidths = np.repeat(self.bandwidths,
                                        self.samples.shape[1]).astype('float64')
            
        elif (isinstance(self.bandwidths,list)) | \
            (isinstance(self.bandwidths,np.ndarray)):
            self.bandwidths = np.array(self.bandwidths)
            for v in range(self.bandwidths):
                assert type(self.bandwidths[i])=='float', \
                    'Value in bandwidths is not a float'
            self.bandwidths = self.bandwidths.astype('float64')
            
        else:
            assert False, \
                'Bandwidths must be a single float or array of floats'



    def get_KDEtypes(self):
        """
        Convert strings to ints that represent kernels
        """
        KDEnames = np.array(['gaussian',
                             'triangular',
                             'epanechnikov',
                             'biweight',
                             'triweight',
                             'tricube',
                             'cosine',
                             'uniform'])
        KDEints  = np.array([0,1,2,3,4,5,6,7])
        
        if isinstance(self.KDEtypes,str):
            self.KDEtypes = np.array([self.KDEtypes])
        
        KDEtypes = np.zeros(len(self.KDEtypes),dtype='int')
        for i in range(self.KDEtypes.shape[0]):
            ind = self.KDEtypes==KDEnames
            if np.any(ind)==False:
                print '\n',KDEnames,'\n'
                assert False, \
                    'KDEname %s not in above list' % self.KDEtypes[i]
            KDEtypes[i] = KDEints[ind]

        if KDEtypes.shape[0]==1:
            KDEtypes = np.repeat(KDEtypes,self.samples.shape[1])

        return KDEtypes.astype('int64')
        
    def _define_KDE_function(self):
        """
        This reads in the compiled KDE library
        """
        try:
            dll = ct.CDLL(self.dll_path,mode=ct.RTLD_GLOBAL)
        except:
            print '\nCompiled KDE library not found in \''+self.dll_path+'\''
            print '\nBuilding in place\n'
            try:
                os.system('python setup.py build_ext --inplace')
                dll = ct.CDLL(self.dll_path,mode=ct.RTLD_GLOBAL)
            except:
                assert False, 'Fail, couldn\'t find setup.py'
        func = dll.KDE
        func.argtypes = [ct.c_long,ct.c_long,ct.POINTER(ct.c_long),
                         ct.POINTER(ct.c_double),ct.POINTER(ct.c_double),
                         ct.POINTER(ct.c_double)]
        self.estimator = func

if __name__=='__main__':
    import matplotlib.pyplot as pl
    k = KDE()

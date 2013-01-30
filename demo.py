
import time
import ctypes 
import numpy as np
import matplotlib.pyplot as pl

from ctypes import c_double,c_long,POINTER

def _load_triweight_KDE_1D(dll_path,function_name):
    """
    This reads in the compiled interpolation library
    """
    dll = ctypes.CDLL(dll_path,mode=ctypes.RTLD_GLOBAL)
    func = dll.triweight_KDE_1D
    func.argtypes = [c_long,POINTER(c_double),c_double,
                     POINTER(c_double)]
    return func

def gaussian_kde(d,h):
    pdf = np.zeros(d.shape[0])
    for i in range(d.shape[0]):
        ref = np.arange(d.shape[0])
        ref = np.delete(ref,i)
        pdf[i] = np.sum(np.exp(-0.5*(d[i]-d[ref])**2./h**2)) / np.sqrt(2.*np.pi*h**2)
    return pdf/(d.shape[0])


if __name__=='__main__':

    triweight_KDE=_load_triweight_KDE_1D('./_triweight_KDE_1D.so',
                                         'triweight_KDE_1D')

    np.random.seed(234)
    data = np.random.randn(1000).astype('float64')
    data[:500] = data[:500]*0.5 + 0.5
    data = np.sort(data)

    h = 0.1 # magic
    gaussian_pdf = gaussian_kde(data,h)

    scaled = data / h
    scaled_p = scaled.ctypes.data_as(POINTER(c_double))
    triweight_pdf = np.zeros(scaled.shape[0]).astype('float64')
    triweight_pdf_p = triweight_pdf.ctypes.data_as(POINTER(c_double))

    triweight_KDE(scaled.shape[0], scaled_p, h, triweight_pdf_p)

    fig = pl.figure()
    pl.hist(data,30,alpha=0.2,normed=True,label='Samples')
    pl.plot(data,gaussian_pdf,'g',lw=2,label='Gaussian KDE')
    pl.plot(data,triweight_pdf,'r',lw=2,label='Triweight KDE')
    pl.legend(loc=2)
    pl.show()
    fig.savefig('demo.png')
    

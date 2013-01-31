//
// Multivariate Kernel Density Estimation. 
// http://en.wikipedia.org/wiki/Multivariate_kernel_density_estimation
// http://en.wikipedia.org/wiki/Kernel_density_estimation
// http://en.wikipedia.org/wiki/Kernel_%28statistics%29
//
//
// Author - Ross Fadely	
//
//

#include <math.h>

double KDE_1D(long,long,long,long,long,double,double*);
void KDE(long,long,long*,double*,double*,double*);

void KDE(long Nsamp, long Ndim,long *KDEtype, double *h, double *samples, double *pdf) {
    //
    // Multivariate KDE, assumes input array (originally Nsamp x Ndim) is flattened.
    //
    
    long i,j;
    
    for (i=0; i<Nsamp; i++) {
        pdf[i] = 0.0;
        for (j=0; j<Ndim; j++) {
            if (j==0) {
                pdf[i] = KDE_1D(Nsamp,Ndim,i,j,KDEtype[j],h[j],samples);
            } else {
                pdf[i] *= KDE_1D(Nsamp,Ndim,i,j,KDEtype[j],h[j],samples);
            }
        }
        pdf[i] *= 1.0 / (double)Nsamp;
    }
    
    
}

double KDE_1D(long Nsamp,long Ndim,long i,long j,long KDEtype,double h, double *samples) {
    //
    // Do a 1D KDE
    //
    
    long k, ind, idx;
    double u, pdf=0.0;
    
    ind = i * Ndim + j; // index of point being estimated
    
    for (k=0; k<Nsamp; k++) {
        
        // index of current sample along the jth dimension
        idx = k * Ndim + j;
        
        // scaled difference
        u = (samples[ind] - samples[idx]) / h;
        
        // begin kernel types
        //
        // Triweight
        if (KDEtype==0) {
            if (ind!=idx && u>-1.0 && u<1.0) {
                pdf += 35. / 32. * pow((1.0 - u * u),3.0);
            }
        }
    }
    
    pdf *= 1.0 / h;
    
    return pdf;
}
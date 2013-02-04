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

double kernel_estimate(long,double,double,double);
void KDE(long,long,long*,double*,double*,double*);

void KDE(long Nsamp, long Ndim,long *KDEtype, double *h, double *samples, double *pdf) {
    //
    // Multivariate KDE, assumes input array (originally Nsamp x Ndim) is flattened.
    //
    
    long i,j,k,ind,idx;
    double KDE_1D;
    
    for (k=0; k<Nsamp; k++) {
        pdf[k] = 0.0;
        for (i=0; i<Nsamp; i++) {
            if (k!=i) {
                for (j=0; j<Ndim; j++) {
                    KDE_1D = 0.0;
                    idx = i * Ndim + j; // examplar (x_exp)
                    ind = k * Ndim + j; // point being estimated (x_est)
                    if (KDE_1D==0.0) {
                        KDE_1D = kernel_estimate(KDEtype[j],h[j],samples[ind],samples[idx]);   
                    } else {
                        KDE_1D *= kernel_estimate(KDEtype[j],h[j],samples[ind],samples[idx]);
                    }
                }
                pdf[k] += KDE_1D;
            }
        }
        pdf[k] *= 1.0 / (double)Nsamp;
    }
    
}

double kernel_estimate(long KDEtype, double h, double x_est, double x_exp) {
    //
    // Return the kernel estimate for the point being estimated (x_est),  
    // using the given examplar (x_exp).
    //
    
    double u, KE=0.0;
    const double pi = 3.14159265359;
    
                
    // scaled difference
    u = (x_est - x_exp) / h;

    // begin kernel types
    //
    // Gaussian
    if (KDEtype==0) {               
        KE = exp(-0.5 * u * u) / sqrt(2. * pi) / h;   
    }
    // Triangular
    if (KDEtype==1) {
        // why is abs() all screwy?
        if (u>-1.0 && u<1.0) {
            KE = 1.0 - sqrt(u * u) / h;
        }
    }
    // Epanechnikov
    if (KDEtype==2) {
        if (u>-1.0 && u<1.0) {
            KE = 3. / 4. * (1.0 - u * u) / h;
        }
    }
    // Biweight
    if (KDEtype==3) {
        if (u>-1.0 && u<1.0) {
            KE = 15. / 16. * pow((1.0 - u * u),2.0) / h;
        }
    }
    // Triweight
    if (KDEtype==4) {
        if (u>-1.0 && u<1.0) {
            KE = 35. / 32. * pow((1.0 - u * u),3.0) / h;
        }
    }
    // Tricube
    if (KDEtype==5) {
        // why is abs() all screwy?
        if (u>-1.0 && u<1.0) {
            KE = 70. / 81. * pow((1.0 - sqrt(pow(u,6.0))),3.0) / h;
        }
    }
    // Cosine
    if (KDEtype==6) {
        if (u>-1.0 && u<1.0) {
            KE = 0.25 * pi * cos(0.5 * pi * u) / h;
        }
    }
    // Uniform
    if (KDEtype==7) {
        if (u>-1.0 && u<1.0) {
            KE = 0.5 / h;
        }
    }
    
    return KE;
}
    
    

//
// Kernel Density Estimation... in 1D... using a triweight kernel. 
// http://en.wikipedia.org/wiki/Kernel_%28statistics%29
//
// Not sure it gets more specialized than that.
//
// Input samples have been scaled by the bandwidth h.
// http://en.wikipedia.org/wiki/Kernel_density_estimation
//
// Author - Ross Fadely	
//
//

void triweight_KDE_1D(long Nsamp, double *scaledsamples, double h,
                      double *pdf) {

    long i, j;
    double u, norm;
    
    norm = 35. / 32. / h / (double)Nsamp;

    for (i=0; i<Nsamp; i++) {
        pdf[i] = 0.0;
        for (j=0; j<Nsamp; j++) {
            u = scaledsamples[i] - scaledsamples[j]
            // Double check that i!=j is not necessary
            if (u>-1.0 && u<1.0) {
                pdf[i] += pow((1.0 - u * u),3.0);
            }
        }
        pdf[i] *= norm;
    }
    
    
}

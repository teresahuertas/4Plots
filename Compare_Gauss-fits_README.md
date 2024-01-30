<<<<<<< HEAD
This code manages the observational and theoretical data of PNe IC 418 and NGC 7027.

- Observational data: fit of each observed line with a Gaussian function. This was done by the tool provided in GILDAS-CLASS.
Parameters:
    - Species: line name
    - Freq[MHz]: line frequency
    - Upper: upper level of the transition
    - Lower: lower level of the transition
    - Area: area of the line
    - Error_area: error of the area
    - Velocity: velocity of the peak
    - Error_vel: error of the velocity
    - FWHM: full width at half maximum
    - Error_FWHM: error of the FWHM
    - Tpeak: peak temperature in K (data was in Tmb)
    - Sigma: standard deviation of the Gaussian
    - RMS line: rms of the line
    - gA:
    - Delta_n: difference between the upper and lower levels
- Theoretical data: results from a ratiative transport modeling (Co3RaL) of each PNe and each element.
Parameters:
    - Species: line name
    - Freq[MHz]: line frequency
    - Vel[km/s]: velocity of the peak
    - Flux[Jy]: flux of the line
    - LTE_corr: correction factor to the LTE approximation
    - Delta_n: difference between the upper and lower levels

Definitions:
- Chemical elements: element = ['H', '3HeI', 'HeI', '3HeII', 'HeII', 'CI', 'OIII']

Data are stored in the following pandas dataframes:
- gildas_fit_data[source + 'fit'][<column_name>]: original data from GILDAS-CLASS fits
- iram[f'{source}_{e}'][<column_name>], where e is the element: IRAM-30m frequencies of GILDAS-CLASS data fits for each source and element. Tpeak is corrected and converted to Jy
- yebes[f'{source}_{e}'][<column_name>], where e is the element: Yebes-40m frequencies of GILDAS-CLASS data fits for each source and element. Tpeak is corrected and converted to Jy
- coral[f'{source}_{e}'][<column_name>], where e is the element: Co3RaL data for each source and element
- emir2[f'{source}_{e}'][<column_name>], where e is the element: EMIR-2 frequencies of GILDAS-CLASS data fits for each source and element
- emir3[f'{source}_{e}'][<column_name>], where e is the element: EMIR-3 frequencies of GILDAS-CLASS data fits for each source and element
- coral_emir2[f'{source}_{e}'][<column_name>], where e is the element: EMIR-2 frequencies of Co3RaL data for each source and element
- coral_emir3[f'{source}_{e}'][<column_name>], where e is the element: EMIR-3 frequencies of Co3RaL data for each source and element
- coral_yebes[f'{source}_{e}'][<column_name>], where e is the element: Yebes-40m frequencies of Co3RaL data for each source and element
=======

>>>>>>> a4fddad2408f6fe647084033e71ab730f7106f37

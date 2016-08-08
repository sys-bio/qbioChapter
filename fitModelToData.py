import pylab as plt; 
import numpy as np
import lmfit;
import tellurium as te; 
import roadrunner
import time; 
import copy; 
import random

#numpy.random.seed (int (time.time()))
np.random.seed (2)
r = te.loada("""
   S1 -> S2; k1*S1;
   S2 -> S3; k2*S2;
   
   S1 = 1; S2 = 0; S3 = 0; 
   k1 = 0.45; k2 = 0.15; 
""")

toFit = ['k1', 'k2']; nParameters = len (toFit)

nDataPoints = 24
# Create the experimental data
m = r.simulate (0, 20, nDataPoints)

x_data = m[:,0]; y_data = m[:,2]
for i in range (0, len (y_data)):
    y_data[i] = y_data[i] + np.random.normal (0, 0.05); # Add noise

# Compute the simulation at the current parameter values
def my_ls_func(p):
    r.reset()  
    pp = p.valuesdict()
    for i in range(0, nParameters):
       r.model[toFit[i]] = pp[toFit[i]]
    m = r.simulate (0, 20, nDataPoints)
    # Just return S2
    return m[:,2]

# Compute the residuals between objective and experimental data
def f_residual(p):
    # Ideally we should accunt for the experimental errors
    # However the lmfit docs are not clear    
    return y_data - my_ls_func (p)
   
# Set up the parameters that we will fit
params = lmfit.Parameters()
params.add('k1', value=10, min=0, max=10)
params.add('k2', value=10, min=0, max=10)

minimizer = lmfit.Minimizer(f_residual, params)
result = minimizer.minimize(method='leastsqr')
lmfit.report_fit(result.params, min_correl=0.5)

# Assign fitted parameters to the model
r.reset()
for i in range(0, nParameters):
   r.model[toFit[i]] = result.params[toFit[i]].value
m = r.simulate (0, 20, 100)

plt.figure (figsize=(7,5))
# Plot experimental data
ldata, = plt.plot (x_data, y_data, 'dk', markersize=10)
# Plot the fitted lines for S1, S2 and S3
# Retrive lfit to use in the legend
lfit, = plt.plot (m[:,0], m[:,1], '-k')
plt.plot (m[:,0], m[:,2], '-k')
plt.plot (m[:,0], m[:,3], '-k')

# Plot the residuals
resids = f_residual (result.params)
lresids, = plt.plot (x_data, resids, 'ko', markersize=6)
plt.vlines(x_data, [0], resids, color='k', linewidth=2)

theResiduals = copy.deepcopy (resids)
finalFittedData = copy.deepcopy (y_data)
originalYData = copy.deepcopy (y_data)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time', fontsize=16)
plt.ylabel("Concentration", fontsize=16)
plt.legend([ldata, lfit, lresids],['data', 'fit', 'residuals'], loc=0)
plt.axhline (y=0, color='k')
plt.savefig('c:\\tmp\\foo.pdf')
plt.show()
 
k1Sample = []; k2Sample = []; NSamples = 1000

# Start the Monte Carlo parameter confidence estimation
for n in range (NSamples): 
   for i in range (len (finalFittedData)):
       y_data[i] = originalYData[i] + random.choice (theResiduals)

   result = minimizer.minimize(method='leastsqr')
   # Not all fits will work so we test against a threshold   
   if result.redchi < 0.01: 
      pp = result.params.valuesdict()
      # Collect the fitted parameters
      k1Sample.append (pp['k1'])
      k2Sample.append (pp['k2'])
   
plt.xlabel('k1', fontsize=16); plt.ylabel('k2', fontsize=16)
plt.plot (k1Sample, k2Sample, '.b')

meank1 = np.mean (k1Sample); meank2 = np.mean (k2Sample)
# Compute 95% percentiles
plusk1 = np.percentile (k1Sample, 97.5) - meank1
minusk1 = meank1 - np.percentile (k1Sample, 5)

plusk2 = np.percentile (k2Sample, 97.5) - meank2
minusk2 = meank2 - np.percentile (k2Sample, 5)

# Note that the limits are not symmetric
print 'Computed 95 percent percentiles'
print meank1, "+/- ", plusk1, minusk1
print meank2, "+/- ", plusk2, minusk2

plt.hist (k1Sample, 12)
plt.ylabel('Frequency'); plt.xlabel ('k1'); plt.title ('k1 variation')
plt.show()
plt.hist (k2Sample, 12)
plt.ylabel('Frequency'); plt.xlabel ('k2'); plt.title ('k2 variation');
plt.show()



import pylab as plt; import numpy as np
import lmfit; import tellurium as te; import roadrunner
import time; import copy; import random

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

# Change this index to use a different variable
S2Index = 2
x_data = m[:,0]; y_data = m[:,S2Index]
y_weight = np.empty([nDataPoints])
for i in range (0, len (y_data)):
    y_weight[i] = 0.05 # standard deviation of noise
    y_data[i] = y_data[i] + np.random.normal (0, y_weight[i]); # Add noise

# Compute the simulation at the current parameter values
def my_ls_func(p):
    r.reset()  
    pp = p.valuesdict()
    for i in range(0, nParameters):
       r.model[toFit[i]] = pp[toFit[i]]
    m = r.simulate (0, 20, nDataPoints)
    # Just return S2
    return m[:,S2Index]

# Compute the residuals between objective and experimental data
def weightedResiduals(p):
    return (y_data - my_ls_func (p))/y_weight
   
def unWeightedResiduals(p):
    return y_data - my_ls_func (p)

# Set up the parameters that we will fit
params = lmfit.Parameters()
params.add('k1', value=10, min=0, max=10)
params.add('k2', value=10, min=0, max=10)

minimizer = lmfit.Minimizer(weightedResiduals, params)
result = minimizer.minimize(method='leastsqr')
lmfit.report_fit(result.params, min_correl=0.5)

# Assign fitted parameters to the model
r.reset()
for i in range(0, nParameters):
   r.model[toFit[i]] = result.params[toFit[i]].value
m = r.simulate (0, 20, 100)

# Set up some convenient font sizes
plt.rcParams.update({'axes.titlesize': 16})
plt.rcParams.update({'axes.labelsize': 14})
plt.rcParams.update({'xtick.labelsize': 13})
plt.rcParams.update({'ytick.labelsize': 13})

#legend.fontsize

plt.figure (figsize=(7,5))
# Plot experimental data
ldata, = plt.plot (x_data, y_data, 'dm', markersize=8)
# Plot the fitted lines for S1, S2 and S3
# Retrive lfit to use in the legend
lfit, = plt.plot (m[:,0], m[:,1], '-g', linewidth=2)
plt.plot (m[:,0], m[:,2], '-g', linewidth=2)
plt.plot (m[:,0], m[:,3], '-g', linewidth=2)

# Plot the residuals
resids = unWeightedResiduals(result.params)
lresids, = plt.plot (x_data, resids, 'bo', markersize=6)
plt.vlines(x_data, [0], resids, color='r', linewidth=2)

theResiduals = copy.deepcopy (resids)
finalFittedData = copy.deepcopy (y_data)
originalYData = copy.deepcopy (y_data)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel('Time')
plt.ylabel("Concentration", fontsize=16)
plt.legend([ldata, lfit, lresids],['Data', 'Best fit', 'Residuals'], loc=0, fontsize=10)
plt.axhline (y=0, color='k')
plt.savefig('fittedCurves.pdf')
plt.show()
 
k1Sample = []; k2Sample = []; NSamples = 5000

chis = []
# Start the Monte Carlo parameter confidence estimation
for n in range (NSamples): 
   for i in range (len (finalFittedData)):
       y_data[i] = originalYData[i] + random.choice (theResiduals)

   result = minimizer.minimize(method='leastsqr')
   # Not all fits will work so we test against a threshold   
   if result.redchi < 4: 
      chis.append (result.redchi)
      pp = result.params.valuesdict()
      # Collect the fitted parameters
      k1Sample.append (pp['k1'])
      k2Sample.append (pp['k2'])
   
# Compute the mean values of the k1 and k2 samples
meank1 = np.mean (k1Sample); meank2 = np.mean (k2Sample)

# Compute 95% percentiles
plusk1 = np.percentile (k1Sample, 97.5) - meank1
minusk1 = meank1 - np.percentile (k1Sample, 2.5)

plusk2 = np.percentile (k2Sample, 97.5) - meank2
minusk2 = meank2 - np.percentile (k2Sample, 2.5)

# Note that the limits are not symmetric
print 'Computed 95 percent percentiles'
print 'k1: ', meank1, "+/- ", plusk1, minusk1
print 'k2: ', meank2, "+/- ", plusk2, minusk2

plt.hist (k1Sample, 12, color='peachpuff')
plt.ylabel('Frequency'); 
plt.xlabel ('k1'); plt.title ('k1 variation')
plt.savefig('k1Distribution.pdf')
plt.show()
plt.hist (k2Sample, 12, color='peachpuff')
plt.ylabel('Frequency'); 
plt.xlabel ('k2'); plt.title ('k2 variation');
plt.savefig('k2Distribution.pdf')
plt.show()

# Scatter plot of k1 versus k2
plt.xlim((0.1, 0.6)); plt.ylim ((0.1, 0.5))
plt.plot (k1Sample, k2Sample, '.', color='cornflowerblue')
plt.xlabel ('k1'); plt.ylabel ('k2')
plt.title ('Scatter plot of k1 against k2')
plt.savefig('k1_k2_scatter.pdf')
plt.show()


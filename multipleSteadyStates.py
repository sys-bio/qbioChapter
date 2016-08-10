# Find multiple steady states
import tellurium as te
import pylab as plt; 

r = te.loada('''
    J1: $Xo -> S1; 0.1 + k1*S1^4/(k2+S1^4);
    S1 ->; k3*S1;
    k1 = 0.9;
    k2 = 0.3;
    k3 = 0.7;
    S1 = 0;
''')

# Set a starting concentation of S1 to find the low steady state
r.S1 = 0.01
r.steadyState()
print "S1 = ", r.S1

# Set a starting concentation of S1 to find the high steady state
r.S1 = 20
r.steadyState()
print "S1 = ", r.S1

# Set a starting concentation of S1 to the midpoint to find the unstable steady state
r.S1 = 0.65
r.steadyState()
print "S1 = ", r.S1

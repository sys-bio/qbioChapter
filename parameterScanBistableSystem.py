# Time course parameter scan of a bistable system
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

S1Ref = 0.1
#result = r.simulate (0, 12, 100, ['time', 'S1'])
for x in plt.arange (0.1, 2, 0.2): 
    m = r.simulate (0, 12, 100, ['Time', 'S1'])
    plt.plot (m[:,0], m[:,1], linewidth=2)  
    S1Ref = S1Ref + 0.1
    r.S1 = S1Ref
    
plt.show()

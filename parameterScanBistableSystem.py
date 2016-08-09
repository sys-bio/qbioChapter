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

S1Initial = 0.1
for x in plt.arange (0.1, 2, 0.2): 
    m = r.simulate (0, 12, 100, ['Time', 'S1'])
    plt.plot (m[:,0], m[:,1], linewidth=2)  
    S1Initial = S1Initial + 0.1
    r.S1 = S1Initial
 
plt.xlabel ('Time', fontsize=16)   
plt.ylabel ('Concentration of S1', fontsize=16)
plt.title ('Bistable system showing high and low states', y=1.08, fontsize=16)
plt.show()

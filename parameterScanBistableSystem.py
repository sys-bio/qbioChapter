 Time course parameter scan of a bistable system
import tellurium as te
import pylab as plt; 

r = te.loada('''
    J1: $Xo -> x; 0.1 + k1*x^4/(k2+x^4);
    x -> $w; k3*x;
    k1 = 0.9;
    k2 = 0.3;
    k3 = 0.7;
    x = 0;
''')

result = r.simulate (0, 12, 100, ['time', 'x'])
for x in plt.arange (0.1, 2, 0.2): 
    r.x = x
    m = r.simulate (0, 12, 100, ['x'], linewidth=2)
    plt.plot (result[:,0], m[:,0])    
    
plt.show()

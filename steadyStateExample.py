
# Example showing the use of the steadyState method

import tellurium as te
import roadrunner

r = te.loada("""
     $Xo -> S1; k1*Xo; 
      S1 -> S2; k2*S1;
      S2 -> $X1; k3*S2;
      
      Xo = 10;
      k1 = 0.4; k2 = 0.56; k3 = 0.2;
""")

r.steadyState()
print "S1 = ", r.S1, "S2 = ", r.S2;

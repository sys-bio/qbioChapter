
# Example showing how model sensitivities can be computed
 
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

# Compute some sensitivities

print "Scaled sensitivity of S1 with respect to k1: ", r.getCC ('S1', 'k1')
print "Uncaled sensitivity of S1 with respect to k1: ", r.getuCC ('S1', 'k1')

print "Scaled sensitivity of S1 with respect to k2: ", r.getCC ('S1', 'k2')
print "Uncaled sensitivity of S1 with respect to k2: ", r.getuCC ('S1', 'k2')

print "Scaled sensitivity of S1 with respect to k3: ", r.getCC ('S1', 'k3')
print "Uncaled sensitivity of S1 with respect to k3: ", r.getuCC ('S1', 'k3')

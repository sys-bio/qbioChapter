
# Simple model with a conserved cycle S1 + S2 = T
# Set the conservedMoietyAnalysis = True for these models 
import tellurium as te
import roadrunner

r = te.loada("""
      S1 -> S2; k1*S1;
      S2 -> S1; k2*S2;
      
      S1 = 6; S2 = 0;
      k1 = 0.3; k2 = 0.56
""")

# Print out any conserved cycles
print r.getConservationMatrix()
# To compute the steady state we must first set the 
r.conservedMoietyAnalysis = True;
r.steadyState();
print 'Steady State levels for S1 and S2 are ', r.S1, r.S2;

# Sniffers, buzzers, toggle and blinker.
# Tyson Model 1d - Adaptation

import tellurium as te
import matplotlib.pyplot as plt

r= te.loada('''
   $src -> x;   k3*S;
       x -> $w; k4*x;
    $src -> R;  k1*S;
       R -> $w; k2*x*R;

   # Perturbations
   at time > 10: S = 2;
   at time > 20: S = 4;
   at time > 30: S = 6;
   at time > 40: S = 8;

   k1 = 2; k2 = 2; 
   k3 = 1; k4 = 1;
   x = 0; S = 0.5;
''')

m = r.simulate (0, 60, 500);

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(m[:,0], m[:,1], 'r-', linewidth=2)
ax1.plot(m[:,0], m[:,2], 'g-', linewidth=2)
ax2.plot(m[:,0], m[:,3], 'b-', linewidth=2)
ax1.set_xlabel('Time', fontsize=16)
ax1.set_ylabel('X', color='g', fontsize=16)
ax2.set_ylabel('S and R', color='b', fontsize=16)
plt.show()

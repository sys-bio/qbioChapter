# Sniffers, buzzers, toggles and blinkers.
# Tyson Model 2c - Substrate-depletion oscillator

import tellurium as te
import matplotlib.pyplot as plt

r = te.loada ('''
   J1: $src -> X;      k1*S;
   J2:    X -> R;     (kop + ko*EP)*X;
   J3:    R -> $waste; k2*R;
   J4:    E -> EP;     Vmax_1*R*E/(Km_1 + E);
   J5:   EP -> E;      Vmax_2*EP/(Km_2 + EP);

   src = 0; kop = 0.01; ko =  0.4;
   k1 = 1;  k2 = 1;     R = 1;
   EP = 1;  S = 0.2;    Km_1 = 0.05;
   Km_2 = 0.05; Vmax_2 = 0.3; Vmax_1 = 1;
''')

m = r.simulate (0, 300, 1000, ["Time", "R", "X", "EP", "E"]);

plt.plot(m[:,0], m[:,1], 'r-', label="R", linewidth=2)
plt.plot(m[:,0], m[:,2], 'g-', label="X", linewidth=2)

plt.legend(loc='upper right')
plt.xlabel('Time', fontsize=16)
plt.ylabel('Concentration', fontsize=16)
plt.show()

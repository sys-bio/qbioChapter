# Example to show how to define events in a model
import tellurium as te

rr = te.loada ('''
     $Xo -> S1;  k1*Xo;
      S1 -> $X1; k2*S1;

     Xo = 10; k1 = 0.3; k2 = 0.15;

     at time > 40: S1 = S1*1.6
''')

m = rr.simulate (0, 80, 100)
rr.plot()

p = LatexExport(r)
p.color = ['blue', 'green', 'red']
p.legend = ['S1']
p.xlabel = 'Time'
p.ylabel = 'Concentration'
p.exportComplete = True
p.exportClipboard = True
p.saveto = 'C:\\tmp'
p.saveToOneFile(m)

url = "http://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000010"

import roadrunner
import matplotlib.pyplot as plt

r = roadrunner.RoadRunner(url)
m = r.simulate (0, 4000, 500)

plt.plot(m[:,0], m[:,1], 'r-', label="MKKK", linewidth=2)
plt.plot(m[:,0], m[:,3], 'b-', label="MKK", linewidth=2)
plt.plot(m[:,0], m[:,6], 'g-', label="MAPK", linewidth=2)
plt.show()

import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
X=load(); s=sample(X,42,100000); m=fit(s,42)
o=ndvi_order(m.cluster_centers_); c=m.cluster_centers_[o]
np.set_printoptions(precision=3,suppress=True,linewidth=150)
print(np.abs(c-REF).max(1))
print(c[:,[2,3]]);print(REF[:,[2,3]])
d=((c[:,None]-REF[None])**2).sum(2); print(d.argmin(1)+1)
print("ref ndvi",(REF[:,3]-REF[:,2])/(REF[:,3]+REF[:,2]))
print("inertia of REF centres on sample:",((s[:,None,:]-REF[None])**2).sum(2).min(1).sum())

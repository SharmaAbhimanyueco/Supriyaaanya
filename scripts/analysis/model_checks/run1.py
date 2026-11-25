import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import json
X=load(); print({y:len(X[y]) for y in YEARS})
res={}
# Task1
s=sample(X,42,100000); m=fit(s,42)
o=ndvi_order(m.cluster_centers_); c=m.cluster_centers_[o]
res["task1"]=dict(n_iter=int(m.n_iter_),inertia=float(m.inertia_),converged_before_max_iter=bool(m.n_iter_<100),max_abs_centre_diff=float(np.abs(c-REF).max()))
cls=[NAMES[i+1] for i in range(10)]
# classify: predicted raw label -> rank
rank=np.empty(10,int); rank[o]=np.arange(10)
isb=np.array([NAMES[r+1]=="Built-up" for r in rank])
res["task1"]["built_up_ha"]={str(y):float(isb[m.predict(X[y])].sum()*0.09) for y in YEARS}
res["task1"]["reference_built_up_ha"]={"2015":6609.1,"2020":9224.1,"2025":14529.4}
print(res["task1"],flush=True)
# Task2
from sklearn.metrics import silhouette_score,davies_bouldin_score,calinski_harabasz_score
i1=np.random.default_rng(0).choice(len(s),20000,replace=False)
i2=np.random.default_rng(1).choice(len(s),50000,replace=False)
ks=list(range(4,17)); t2=dict(k=ks,inertia=[],silhouette=[],davies_bouldin=[],calinski_harabasz=[])
for k in ks:
    mk=fit(s,42,n_init=3,k=k); l=mk.labels_
    t2["inertia"].append(float(mk.inertia_))
    t2["silhouette"].append(float(silhouette_score(s[i1],l[i1])))
    t2["davies_bouldin"].append(float(davies_bouldin_score(s[i2],l[i2])))
    t2["calinski_harabasz"].append(float(calinski_harabasz_score(s[i2],l[i2])))
    print(k,t2["inertia"][-1],t2["silhouette"][-1],t2["davies_bouldin"][-1],t2["calinski_harabasz"][-1],flush=True)
x=np.array(ks,float);y=np.array(t2["inertia"])
xn=(x-x.min())/(x.max()-x.min()); yn=(y-y.min())/(y.max()-y.min())
# distance to chord from first to last point
d=np.abs((yn[-1]-yn[0])*xn-(xn[-1]-xn[0])*yn+xn[-1]*yn[0]-yn[-1]*xn[0])/np.hypot(xn[-1]-xn[0],yn[-1]-yn[0])
t2["elbow_distances"]=d.tolist(); t2["elbow_k"]=int(ks[int(d.argmax())])
t2["best_silhouette_k"]=int(ks[int(np.argmax(t2["silhouette"]))])
t2["best_db_k"]=int(ks[int(np.argmin(t2["davies_bouldin"]))]); t2["best_ch_k"]=int(ks[int(np.argmax(t2["calinski_harabasz"]))])
print("elbow",t2["elbow_k"],t2["best_silhouette_k"],t2["best_db_k"],t2["best_ch_k"])
res["task2"]=t2
# Task3
v25=X[2025]; sub=np.random.default_rng(7).choice(len(v25),200000,replace=False); Xs=v25[sub]
ref_lab=rank[m.predict(Xs)]; ref4=np.array([NAMES[r+1] for r in range(10)])[ref_lab]
from sklearn.metrics import adjusted_rand_score
runs={}
for sd in [1,2,3,4,5]:
    ms=fit(sample(X,sd,100000),sd); cl=ref_class_of_centres(ms.cluster_centers_)
    r=dict(built_up_ha=built_ha(ms,X,cl))
    lab=ms.predict(Xs); r["ari"]=float(adjusted_rand_score(ref_lab,lab)); r["agreement4_pct"]=float((cl[lab]==ref4).mean()*100)
    r["n_iter"]=int(ms.n_iter_); r["n_builtup_clusters"]=int((cl=="Built-up").sum())
    r["built_up_ha"]={str(k):v for k,v in r["built_up_ha"].items()}
    runs[str(sd)]=r; print(sd,r,flush=True)
stab={}
for y in YEARS:
    v=np.array([runs[k]["built_up_ha"][str(y)] for k in runs])
    stab[str(y)]=dict(mean=float(v.mean()),min=float(v.min()),max=float(v.max()),cv_pct=float(v.std(ddof=1)/v.mean()*100),reference=res["task1"]["built_up_ha"][str(y)])
res["task3"]=dict(runs=runs,summary=stab,cv_note="CV uses sample std (ddof=1)")
print(stab)
# Task4
t4={}
for n in [50000,100000,200000]:
    mn=fit(sample(X,42,n),42); cl=ref_class_of_centres(mn.cluster_centers_)
    t4[str(n)]=built_ha(mn,X,cl); t4[str(n)]={str(k):v for k,v in t4[str(n)].items()}; print(n,t4[str(n)],flush=True)
res["task4"]=t4
json.dump(res,open("model_checks.json","w"),indent=1)

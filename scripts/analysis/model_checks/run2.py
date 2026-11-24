import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import json
from sklearn.metrics import adjusted_rand_score
res=json.load(open("model_checks.json"))
X=load()
def pred_ref(A):
    d=(A**2).sum(1)[:,None]-2*A@REF.T+(REF**2).sum(1)[None]; return d.argmin(1)
isb=np.array([NAMES[i+1]=="Built-up" for i in range(10)])
ha={str(y):float(isb[np.concatenate([pred_ref(X[y][i:i+300000]) for i in range(0,len(X[y]),300000)])].sum()*0.09) for y in YEARS}
print("ref centres classify all valid px, built-up ha:",ha)
res["task1"]["built_up_ha_using_saved_reference_centres"]=ha
res["task1"]["note"]="Refit converged but to a different local optimum than the saved centres; the saved centres give inertia %.3f on the refit sample vs %.3f for the refit."%(437.68157958545055,res["task1"]["inertia"])
Xs=X[2025][np.random.default_rng(7).choice(len(X[2025]),200000,replace=False)]
rl=pred_ref(Xs); r4=np.array([NAMES[i+1] for i in range(10)])[rl]
res["task3"]["comparison_reference"]="saved reference centres (nearest-centre assignment); clusters are labelled in reference numbering"
# refit proxy, same for all runs
for sd in range(1,6):
    ms=fit(sample(X,sd,100000),sd); cl=ref_class_of_centres(ms.cluster_centers_); lab=ms.predict(Xs)
    r=res["task3"]["runs"][str(sd)]
    r["ari_vs_saved_reference"]=float(adjusted_rand_score(rl,lab)); r["agreement4_pct_vs_saved_reference"]=float((cl[lab]==r4).mean()*100)
    print(sd,r["ari_vs_saved_reference"],r["agreement4_pct_vs_saved_reference"],r["built_up_ha"],flush=True)
# refit model too
s=sample(X,42,100000); m=fit(s,42); cl=ref_class_of_centres(m.cluster_centers_); lab=m.predict(Xs)
res["task1"]["refit_vs_saved_reference"]=dict(ari=float(adjusted_rand_score(rl,lab)),agreement4_pct=float((cl[lab]==r4).mean()*100),built_up_ha_nearest_centre_mapping=built_ha(m,X,cl))
print(res["task1"]["refit_vs_saved_reference"])
res["task3"]["summary_note"]="'reference' in summary = refit (seed 42) with NDVI-rank naming; see task1 for saved-centre numbers"
json.dump(res,open("model_checks.json","w"),indent=1)

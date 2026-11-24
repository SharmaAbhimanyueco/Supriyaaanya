import json,numpy as np,matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
r=json.load(open("model_checks.json")); t=r["task2"]; ref={"2015":6609.1,"2020":9224.1,"2025":14529.4}
for y in ref: r["task3"]["summary"][y]["reference_saved"]=ref[y]; r["task3"]["summary"][y]["range_ha"]=r["task3"]["summary"][y]["max"]-r["task3"]["summary"][y]["min"]
r["task3"]["summary"]["note"]="'reference' = refit seed 42; 'reference_saved' = published reference ha"
json.dump(r,open("model_checks.json","w"),indent=1)
plt.rcParams.update({"font.size":14})
fig,ax=plt.subplots(1,2,figsize=(16,8),dpi=100,facecolor="white")
for a,key,tt,yl in [(ax[0],"inertia","Elbow check: how much the clusters tighten as k grows","Within-cluster spread (inertia)"),(ax[1],"silhouette","Separation check (silhouette: higher = clearer groups)","Silhouette score")]:
    a.plot(t["k"],t[key],"o-",color="#1f77b4",lw=2); a.axvline(10,ls="--",color="#d62728")
    a.text(10.15,a.get_ylim()[1]-0.05*(a.get_ylim()[1]-a.get_ylim()[0]),"k = 10 (used)",color="#d62728",va="top")
    a.set_title(tt,fontsize=14); a.set_xlabel("Number of clusters (k)"); a.set_ylabel(yl)
    a.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("k_selection.png"); plt.close()
fig,a=plt.subplots(figsize=(16,8),dpi=100,facecolor="white")
for i,y in enumerate(["2015","2020","2025"]):
    v=[r["task3"]["runs"][s]["built_up_ha"][y] for s in "12345"]
    a.scatter(np.full(5,i)+np.linspace(-0.1,0.1,5),v,s=90,color="#1f77b4",zorder=3,label="Re-run (5 seeds)" if i==0 else None)
    a.hlines(ref[y],i-0.25,i+0.25,color="#d62728",lw=3,label="Reference model" if i==0 else None)
a.set_xticks(range(3)); a.set_xticklabels(["2015","2020","2025"]); a.set_ylabel("Built-up area (ha)")
a.set_title("Same answer when retrained? Built-up area across 5 re-runs"); a.legend(frameon=False); a.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("stability.png"); plt.close()

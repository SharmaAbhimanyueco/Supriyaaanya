import numpy as np, rasterio
S="/tmp/claude-0/-home-user-Supriyaaanya/20e51722-c7b0-52dd-afd3-ffdd0c1c58a6/scratchpad"
YEARS=[2015,2020,2025]
NAMES={1:"Bare",2:"Built-up",3:"Bare",4:"Trees",5:"Cropland",6:"Trees",7:"Cropland",8:"Cropland",9:"Cropland",10:"Cropland"}
CLS=["Built-up","Cropland","Trees","Bare"]
inside=np.load(f"{S}/analysis/inside.npy")
REF=np.load(f"{S}/analysis/pooled_centres.npy")
def load():
    out={}
    for y in YEARS:
        with rasterio.open(f"{S}/analysis/composite_{y}.tif") as r: a=r.read()
        v=inside&np.all(a!=-32768,axis=0)
        out[y]=(a[:,v].T.astype(np.float64)/10000)
    return out
def sample(X,seed,n):
    rng=np.random.default_rng(seed)
    return np.vstack([X[y][rng.choice(len(X[y]),n,replace=False)] for y in YEARS])
def fit(s,rs,n_init=5,k=10):
    from sklearn.cluster import KMeans
    return KMeans(n_clusters=k,n_init=n_init,max_iter=100,random_state=rs).fit(s)
def ndvi_order(c):
    nd=(c[:,3]-c[:,2])/(c[:,3]+c[:,2]); return np.argsort(nd)
def ref_class_of_centres(c):
    d=((c[:,None,:]-REF[None])**2).sum(2); return np.array([NAMES[i+1] for i in d.argmin(1)])
def built_ha(m,X,cls_of):
    isb=np.array([c=="Built-up" for c in cls_of])
    return {y:float(isb[m.predict(X[y])].sum()*0.09) for y in YEARS}

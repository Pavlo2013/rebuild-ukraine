import json,subprocess,re,time
from pathlib import Path
work=Path('work/catalog-step5');assets=Path('outputs/rebuild-ukraine-ui/assets')
choices={'hydro':2,'nuclear':0,'wind':0,'mine':1,'steel':0,'timber':1,'fish':0,'oil':2,'grain':0,'field':0,'greenhouse':2,'port':1,'bridge':2,'rail':0,'hospital':0,'shop':1,'office':1,'water':0}
credits=[]
for name,index in choices.items():
 pages=list(json.loads((work/(name+'.json')).read_text())['query']['pages'].values());p=pages[index];info=p['imageinfo'][0]
 r=subprocess.run(['curl','-fsSL','--retry','2','--max-time','30',info['thumburl'],'-o',str(assets/(name+'.jpg'))],capture_output=True,text=True)
 print(name,r.returncode,flush=True)
 if r.returncode==0:
  meta=info['extmetadata'];clean=lambda v:re.sub('<[^>]*>','',v)
  credits.append(f"- {name}.jpg — {clean(meta.get('Artist',{}).get('value','Unknown'))}; {meta.get('LicenseShortName',{}).get('value','')}; source: {info['descriptionurl']}; license: {meta.get('LicenseUrl',{}).get('value','')}")
 time.sleep(.3)
with Path('outputs/rebuild-ukraine-ui/ASSETS.md').open('a')as f:f.write('\n## Step 5 catalog photographs\n\nThese photos illustrate object types and may show locations outside Ukraine.\n\n'+'\n'.join(credits)+'\n')

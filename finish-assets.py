import json,subprocess,urllib.parse,re
from pathlib import Path
work=Path('work/rebuild-ukraine');root=Path('outputs/rebuild-ukraine-ui/assets');credits=json.loads((work/'credits.json').read_text())
params={'action':'query','generator':'search','gsrsearch':'"Модульне містечко" filetype:bitmap','gsrnamespace':6,'gsrlimit':5,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':640,'format':'json'}
data=json.loads(subprocess.check_output(['curl','-fsSL','https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)]));(work/'modular-final.json').write_text(json.dumps(data));print([p['title']for p in data.get('query',{}).get('pages',{}).values()])
choices={'road':('road2-photos.json',5),'worker':('worker2-photos.json',5)}
if data.get('query',{}).get('pages'):choices['modular']=('modular-final.json',0)
else:choices['modular']=('house-photos.json',0)
for name,(filename,index) in choices.items():
 p=list(json.loads((work/filename).read_text())['query']['pages'].values())[index];info=p['imageinfo'][0];subprocess.run(['curl','-fsSL',info['thumburl'],'-o',str(root/(name+'.jpg'))],check=True);credits.append({'asset':name+'.jpg','source':info['descriptionurl'],'metadata':info['extmetadata']})
(work/'credits.json').write_text(json.dumps(credits))
lines=['# Assets and licenses','\nPhotographs are illustrative reference images, not documentation of the fictional city. All are displayed as supplied, with CSS crops.\n']
for c in credits:
 m=c['metadata'];artist=re.sub('<[^>]+>','',m.get('Artist',{}).get('value',''));lic=m.get('LicenseShortName',{}).get('value','');lines.append(f"- {c['asset']} — {artist}; {lic}; source: {c['source']}; license: {m.get('LicenseUrl',{}).get('value','')}")
lines+=['\nMap: geoBoundaries UKR ADM1, OpenStreetMap / Wambacher, ODbL 1.0. https://www.geoboundaries.org/api/current/gbOpen/UKR/ADM1/','\nReact 18.3.1 and Three.js 0.170.0: MIT. htm 3.1.1: Apache-2.0. D3 7.9.0: ISC. Lucide: ISC. Inter: SIL Open Font License.']
Path('outputs/rebuild-ukraine-ui/ASSETS.md').write_text('\n'.join(lines))

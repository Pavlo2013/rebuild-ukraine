import json,subprocess,urllib.parse,concurrent.futures
from pathlib import Path
work=Path('work/rebuild-ukraine');root=Path('outputs/rebuild-ukraine-ui/assets')
queries={'road2':'asphalt road construction paving','modular2':'modular town Irpin','worker2':'construction worker hard hat portrait -pdf','engineer':'engineer portrait helmet -pdf'}
def query(item):
 key,q=item;params={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':6,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':640,'format':'json'}
 data=json.loads(subprocess.check_output(['curl','-fsSL','https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)]));(work/(key+'-photos.json')).write_text(json.dumps(data));return key,[(p['title'],p['imageinfo'][0].get('thumbwidth'),p['imageinfo'][0].get('thumbheight'))for p in data.get('query',{}).get('pages',{}).values()]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for r in pool.map(query,queries.items()):print(r)
choices={'block':('block',0),'house':('house',0),'school':('school',2),'crane':('crane',1),'solar':('solar',1)}
credits=[]
for name,(queryname,index) in choices.items():
 pages=list(json.loads((work/(queryname+'-photos.json')).read_text())['query']['pages'].values());p=pages[index];info=p['imageinfo'][0];subprocess.run(['curl','-fsSL',info['thumburl'],'-o',str(root/(name+'.jpg'))],check=True);credits.append({'asset':name+'.jpg','source':info['descriptionurl'],'metadata':info['extmetadata']})
(work/'credits.json').write_text(json.dumps(credits))
print('geo',len(json.loads((root/'ukraine-oblasts.geojson').read_text())['features']))

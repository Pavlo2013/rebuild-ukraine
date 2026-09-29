import json,urllib.request,urllib.parse,concurrent.futures,re,subprocess
from pathlib import Path
work=Path('work/rebuild-ukraine');root=Path('outputs/rebuild-ukraine-ui/assets')
queries={'road':'roadworks Ukraine asphalt','block':'apartment building Kyiv modern','modular':'modular housing Ukraine','house':'modern house Ukraine','worker':'construction worker portrait hard hat','school':'school building Ukraine','crane':'tower crane construction','solar':'solar power plant Ukraine'}
def get(item):
 key,q=item
 params={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':6,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':640,'format':'json'}
 try:
  data=json.loads(subprocess.check_output(['curl','-fsSL','https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)]))
  (work/(key+'-photos.json')).write_text(json.dumps(data))
  return key,[(p['title'],p['imageinfo'][0].get('thumbwidth'),p['imageinfo'][0].get('thumbheight')) for p in data.get('query',{}).get('pages',{}).values()]
 except Exception as e:return key,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for row in pool.map(get,queries.items()):print(row)
meta=json.loads((work/'geo-meta.json').read_text());subprocess.run(['curl','-fsSL',meta['simplifiedGeometryGeoJSON'],'-o',str(root/'ukraine-oblasts.geojson')],check=True)

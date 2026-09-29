import json,subprocess,urllib.parse,time
from pathlib import Path
work=Path('work/catalog-step5');assets=Path('outputs/rebuild-ukraine-ui/assets')
queries={'steel':'steelworks plant','timber':'sawmill building logs','grain':'grain elevator silos','greenhouse':'greenhouse building','port':'Odessa port crane','bridge':'Dnipro bridge','rail':'Lviv railway station building','hospital':'hospital building Ukraine','shop':'supermarket building Ukraine','office':'Kyiv office building','water':'wastewater treatment plant'}
for key,q in queries.items():
 args={'action':'query','generator':'search','gsrsearch':q+' filetype:bitmap','gsrnamespace':6,'gsrlimit':3,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':640,'format':'json'}
 r=subprocess.run(['curl','-fsSL','--max-time','20','https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(args)],capture_output=True,text=True)
 if r.returncode:print(key,'failed',flush=True)
 else:
  data=json.loads(r.stdout);(work/(key+'.json')).write_text(json.dumps(data));print(key,[(p['title'])for p in data.get('query',{}).get('pages',{}).values()],flush=True)
 time.sleep(2)

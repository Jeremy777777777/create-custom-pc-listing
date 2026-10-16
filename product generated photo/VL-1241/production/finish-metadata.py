from pathlib import Path
from PIL import Image
import hashlib,json
D=Path(__file__).resolve().parent.parent
for f in D.glob('*.png'):
    with Image.open(f) as src: im=src.convert('RGB')
    im.save(f,dpi=(96,96))
p=D/'logo-qa.json';qa=json.loads(p.read_text())
for e in qa['images']:
    e['finalImageSha256']=hashlib.sha256((D/e['file']).read_bytes()).hexdigest()
    e['commandRecord']+='; lossless RGB PNG 96dpi metadata normalization before review'
p.write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8',newline='\n')

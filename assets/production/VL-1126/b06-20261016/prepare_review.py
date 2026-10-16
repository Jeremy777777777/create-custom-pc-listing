from pathlib import Path
import sys
P=Path(__file__).resolve().parent
root=next((a for a in P.parents if (a/'scripts/gallery_engine.py').exists()),P.parents[1]/'tmp/listing-20744-20261013')
sys.path.insert(0,str(root/'scripts'))
import gallery_engine as g
g.finalize(P/'gallery',P/'layers/lenovo-logo-transparent.png','Lenovo',P/'gallery-contact.png')
from PIL import Image,ImageDraw,ImageCms
# Final compositing preserves RGB pixels; explicitly restore sRGB and DPI metadata.
qa=g.read(P/'gallery/logo-qa.json')
for entry in qa['images']:
 target=P/'gallery'/entry['file'];im=Image.open(target).convert('RGB')
 im.save(target,dpi=(96,96),icc_profile=(P/'layers/sRGB.icc').read_bytes())
 entry['finalImageSha256']=g.digest(target)
g.write(P/'gallery/logo-qa.json',qa)
g.contact_sheet(P/'gallery',P/'gallery-contact.png')
thumbs=Image.new('RGB',(800,720),'#eef3f8');d=ImageDraw.Draw(thumbs)
for i,n in enumerate(g.NAMES):
 im=Image.open(P/'gallery'/n).convert('RGB');im.thumbnail((200,200));x=(i%4)*200;y=(i//4)*240
 thumbs.paste(im,(x,y));d.text((x+2,y+205),n if n.startswith('PT') else 'MAIN '+str(i+1),fill='black')
thumbs.save(P/'gallery-thumbnails.png')
print('Composition prepared for actual visual review; no PASS asserted')

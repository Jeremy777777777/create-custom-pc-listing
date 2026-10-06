from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
import json,hashlib
ROOT=Path(__file__).parent.resolve();SRC=ROOT/'sources'
REPO=next((p for p in ROOT.parents if (p/'scripts/gallery_engine.py').exists()),ROOT.parents[1]/'tmp/business-laptop-redesign-20261005')
source=Image.open(SRC/'official-front.jpg').convert('RGB')
W,H=1075,950;crop=(480,540,1555,1490)
outline=[(617,563),(626,555),(1400,555),(1408,563),(1409,1081),(1407,1090),(1410,1110),(1443,1200),(1482,1300),(1523,1400),(1533,1430),(1533,1438),(1527,1448),(499,1448),(491,1438),(491,1430),(509,1400),(543,1300),(563,1250),(582,1200),(605,1150),(613,1110),(614,1090),(616,565)]
alpha=Image.new('L',source.size);ImageDraw.Draw(alpha).polygon(outline,fill=255)
# The exact OEM neutral-gray chassis is surrounded by a colored campaign scene.
# Remove only colored campaign pixels within the narrow measured silhouette edge;
# LCD pixels are completely replaced below. No keys, ports or marks are redrawn.
ap=alpha.load();sp=source.load()
for y in range(1080,1450):
    for x in range(480,1555):
        if ap[x,y] and max(sp[x,y])-min(sp[x,y])>25:ap[x,y]=0
alpha=alpha.filter(ImageFilter.MinFilter(3))
alpha.save(SRC/'main-product-mask.png')
source=source.convert('RGBA');source.putalpha(alpha)
lcd=(627,578,1400,1013)
art=Image.open(SRC/'approved-cinematic-reference.png').convert('RGB').crop((144,49,1296,561))
scene=ImageOps.fit(art,(lcd[2]-lcd[0],lcd[3]-lcd[1]),method=Image.Resampling.LANCZOS)
scene.save(SRC/'main-screen-art.png')
screenmask=Image.new('L',source.size);ImageDraw.Draw(screenmask).rectangle((lcd[0],lcd[1],lcd[2]-1,lcd[3]-1),fill=255)
screenmask.save(SRC/'main-lcd-mask.png')
source.paste(scene,(lcd[0],lcd[1]))
# Shared lower-screen fade, not individual configuration boxes.
d=ImageDraw.Draw(source)
for y in range(895,1013):
    opacity=int(120+70*(y-895)/118)
    layer=Image.new('RGBA',(773,1),(6,5,10,opacity));source.alpha_composite(layer,(627,y))
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/bahnschrift.ttf',n)
for cx,a,b in [(692,'15.6” FHD','144Hz'),(823,'Ryzen 7','7445HS'),(954,'RTX 4050','6GB'),(1085,'16GB','DDR5'),(1216,'512GB','SSD')]:
    for y,s,n in [(936,a,24),(972,b,22)]:
        bb=d.textbbox((0,0),s,font=font(n));d.text((cx-(bb[2]-bb[0])/2,y),s,font=font(n),fill='white')
win=Image.open(REPO/'assets/branding/windows-11-pro-package.png').convert('RGBA');ww=78;wh=round(ww*win.height/win.width)
win=win.resize((ww,wh),Image.Resampling.LANCZOS);source.alpha_composite(win,(1310,916))
assert 1310+ww<lcd[2] and 916+wh<lcd[3]
cut=source.crop(crop);cut.save(SRC/'main-product-native-cutout.png')
canvas=Image.new('RGBA',(W,H),'white')
shadow=Image.new('RGBA',(W,H));ImageDraw.Draw(shadow).ellipse((40,890,1040,930),fill=(0,0,0,42));shadow=shadow.filter(ImageFilter.GaussianBlur(10));canvas.alpha_composite(shadow)
canvas.alpha_composite(cut)
out=ROOT/'MAIN-ENHANCED-FRONT-CANDIDATE.png'
canvas.convert('RGB').save(out,dpi=(72,72),icc_profile=(SRC/'sRGB.icc').read_bytes())
thumb=canvas.convert('RGB');thumb.thumbnail((200,200));thumb.save(ROOT/'main-200px.png')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
recipe={'schemaVersion':1,'internalId':'VL-1221','scope':'MAIN-ENHANCED-FRONT-CANDIDATE.png','canvas':[W,H],'sourceNativeSize':[2000,2000],'sourcePath':'sources/official-front.jpg','sourceUrl':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/273a1534-d598-474e-8d4a-e1b1d7ca3e59.jpg','sourceSha256':sha(SRC/'official-front.jpg'),'sourceRights':'USER_CONFIRMED_CATALOG_WIDE: HP original exact-model product photo in manufacturer campaign gallery. All third-party game scene and screen content excluded by measured product/LCD masks.','productScale':1,'sourceCrop':crop,'sourceProductOutline':outline,'productMaskSha256':sha(SRC/'main-product-mask.png'),'sourceLcdRectangle':lcd,'lcdMaskSha256':hashlib.sha256(screenmask.tobytes()).hexdigest(),'screenSceneSource':'sources/approved-cinematic-reference.png','screenSceneSourceSha256':sha(SRC/'approved-cinematic-reference.png'),'screenSceneCrop':[144,49,1296,561],'screenSceneRole':'Only the original generated cinematic artwork, never reference chassis or generated text/logos.','font':'Bahnschrift','fontSha256':sha('C:/Windows/Fonts/bahnschrift.ttf'),'fontSizes':[24,22],'windowsMode':'WINDOWS_11_PRO_PACKAGE','windowsAsset':'assets/branding/windows-11-pro-package.png','windowsAssetSha256':sha(REPO/'assets/branding/windows-11-pro-package.png'),'windowsPlacementSourcePixels':[1310,916,ww,wh],'styleOverride':'Direct user no VICTUS marketing title and no configuration frames; preserves exact factory marks and one original Windows package in LCD.','finalSha256':sha(out),'publicationEligibility':'NOT_ASSESSED'}
recipe.update(lcdMaskPath='sources/main-lcd-mask.png',lcdMaskEncoding='SHA256 of native binary-mask pixel bytes, before PNG encoding')
(ROOT/'main-recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
print('Rendered native-source front candidate:',out)

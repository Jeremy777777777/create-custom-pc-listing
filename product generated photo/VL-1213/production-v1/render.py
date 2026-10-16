"""Original OEM product pixels + ImageGen scenes + deterministic text/identity layers.
Invoked Listing rules explicitly require deterministic composition. No AI-redrawn hardware.
"""
import sys, json, hashlib, shutil, math
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter, ImageOps

WORK=Path(__file__).resolve().parent
REPO=WORK.parents[2] if WORK.name=='production-v1' else WORK.parents[1]/'tmp/listing-20744-20261013'
OUT=REPO/'product generated photo/VL-1213'
PROD=OUT/'production-v1'
REF=PROD/'references'
LAY=PROD/'layers'
for p in [OUT,PROD,REF,LAY,OUT/'unbranded']:
    p.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(REPO/'scripts'))
import gallery_engine as g

def write(p,o): g.write(p,o)
def load(p): return Image.open(p).convert('RGBA')
def save(im,p): im.convert('RGB').save(p,dpi=(96,96),**({'quality':96,'subsampling':0} if p.suffix=='.jpg' else {}))
for p in (WORK/'references').glob('*.png'):
    if p.name.startswith('ThinkPad') or p.name in ['front.png','lenovo-logo-official.png']:
        if p.resolve()!=(REF/p.name).resolve(): shutil.copyfile(p,REF/p.name)
for p in (WORK/'layers').glob('*.png'):
    if p.resolve()!=(LAY/p.name).resolve(): shutil.copyfile(p,LAY/p.name)
shutil.copyfile(REPO/'assets/branding/windows-11-pro-lockup.png',REF/'windows-11-pro-lockup.png')
shutil.copyfile(REPO/'assets/branding/windows-11-pro-package.png',REF/'windows-11-pro-package.png')
if (WORK/'style-preview-B15-BG15.png').exists(): shutil.copyfile(WORK/'style-preview-B15-BG15.png',PROD/'approved-style-preview.png')

FONT=Path('C:/Windows/Fonts')
def font(size,bold=False): return ImageFont.truetype(str(FONT/('arialbd.ttf' if bold else 'arial.ttf')),size)
WHITE='#F5F7FA'; MUTED='#B6C5D3'; BLUE='#89CDFA'; DARK='#111E2D'
def text(im,xy,s,size=40,fill=WHITE,bold=False): ImageDraw.Draw(im).text(xy,s,font=font(size,bold),fill=fill,stroke_width=0)
def lines(im,xy,ss,size=40,fill=WHITE,bold=False,step=None):
    for i,s in enumerate(ss): text(im,(xy[0],xy[1]+i*(step or round(size*1.18))),s,size,fill,bold)
def line(im,pts,fill=BLUE,width=3): ImageDraw.Draw(im).line(pts,fill=fill,width=width)
def blank(light=False):
    im=Image.new('RGBA',(1536,1024),'#FFFFFF' if light else '#101D2B')
    d=ImageDraw.Draw(im)
    if not light:
        for x in range(950,1536,100): d.line([(x,210),(x-190,1024)],fill='#1E3348',width=1)
        d.rectangle((0,1008,1536,1024),fill='#315470')
    return im
def header(im,category,title,subtitle=None,light=False):
    col=DARK if light else WHITE
    text(im,(74,52),'THINKPAD P16v GEN 3  /  '+category,25,'#49677F' if light else MUTED,True)
    text(im,(74,115),title,72,col,True)
    if subtitle: text(im,(78,208),subtitle,34,'#49677F' if light else MUTED)
def original(n): return REF/('ThinkPad_P16v_Gen_3_Intel_'+n+'.png')

# Edge-connected neutral background extraction, preserving white key legends.
products={}
for name,n in [('front','CT1_01'),('lid','CT2_05')]:
    dest=LAY/(name+'-cutout.png')
    g.remove_background(original(n),dest)
    im=load(dest); box=im.getchannel('A').getbbox(); im=im.crop(box); im.save(dest)
    if name=='front':
        # OEM neutral floor shadow ends below the chassis. Trim only that shadow,
        # retaining the complete physical base ending above source row 1031.
        im=im.crop((0,0,im.width,1031-box[1]));im.save(dest)
        px=im.load()
        for yy in range(max(0,1000-box[1]),im.height):
            for xx in range(im.width):
                r,gg,b,a=px[xx,yy]
                if min(r,gg,b)>120 and max(r,gg,b)-min(r,gg,b)<20:
                    px[xx,yy]=(r,gg,b,0)
        im.save(dest)
    products[name]=(im,box)

front,frontbox=products['front']
screenpoly=[(637-frontbox[0],243-frontbox[1]),(1370-frontbox[0],243-frontbox[1]),(1370-frontbox[0],701-frontbox[1]),(637-frontbox[0],701-frontbox[1])]
screen=load(LAY/'architectural-screen.png')

def replace_front(source,content):
    result=source.copy(); x0,y0=screenpoly[0]; x1,y1=screenpoly[2]
    result.alpha_composite(content.resize((x1-x0,y1-y0),Image.Resampling.LANCZOS),(x0,y0))
    return result
scene_front=replace_front(front,screen)
scene_front.save(LAY/'front-scene-master.png')
scene_work=replace_front(front,ImageOps.mirror(screen))
blueprint=Image.new('RGBA',(730,457),'#142335'); bd=ImageDraw.Draw(blueprint)
for x in range(40,710,38): bd.line([(x,30),(x,430)],fill='#294156',width=1)
for y in range(30,450,38): bd.line([(30,y),(700,y)],fill='#294156',width=1)
for box in [(110,85,600,360),(125,100,360,345),(380,100,580,230),(380,250,580,345)]:bd.rectangle(box,outline='#A5D3ED',width=4)
bd.line([(220,100),(220,345)],fill='#A5D3ED',width=3)
scene_blueprint=replace_front(front,blueprint)
scene_battery=replace_front(front,ImageOps.fit(load(LAY/'architectural-stage.png').crop((0,0,1536,615)),(730,457)))

def put(im,asset,x,y,w=None):
    obj=asset.copy()
    if w is not None:
        assert w<=obj.width, 'No original product enlargement'
        obj=obj.resize((w,round(obj.height*w/obj.width)),Image.Resampling.LANCZOS)
    im.alpha_composite(obj,(x,y))
    return {'x':x,'y':y,'width':obj.width,'height':obj.height,'label':'PRODUCT_SILHOUETTE'}

# Fixed approved white Windows artwork: deterministic background extraction.
win=load(REF/'windows-11-pro-lockup.png')
extracted=Image.new('RGBA',win.size)
extracted.putdata([(255,255,255,round(max(0,min(1,(r-max(0,b-r)*0.12)/255))*255)) for r,gg,b,a in win.getdata()])
# White identity occupies this measured crop; exclude the blue lower wallpaper.
extracted=extracted.crop((48,78,826,335))
extracted.save(LAY/'windows-lockup-transparent.png')

placement={}; recipes={}; semantics={}
def pt(n,im,zones,facts,notes):
    filename=f'PT{n:02}.png'
    save(im,OUT/'unbranded'/filename)
    placement[filename]={'x':1288,'y':58,'width':168,'height':56,'style':'transparent','protectedZones':zones}
    recipes[filename]={'canvas':list(im.size),'productZones':zones,'sourceMethod':'ORIGINAL_PHOTO','notes':notes}
    semantics[filename]={'primaryFactIds':facts,'notes':notes}

# Strict MAIN preserves OEM product photograph, including original LCD wallpaper.
strict=Image.new('RGBA',(1120,950),'white'); put(strict,front,34,45)
save(strict,OUT/'MAIN-STRICT.jpg')
recipes['MAIN-STRICT.jpg']={'canvas':list(strict.size),'sourceMethod':'ORIGINAL_PHOTO','productBounds':[34,45,front.width,front.height],'screen':'Unmodified OEM reference'}

# Enhanced front, all graphic information stays in the real 16:10 LCD.
lcd=ImageOps.fit(screen,(730,457)).convert('RGBA')
shade=Image.new('RGBA',lcd.size); sd=ImageDraw.Draw(shade); sd.rectangle((0,0,730,148),fill=(7,18,31,185)); lcd.alpha_composite(shade)
text(lcd,(28,22),'ThinkPad P16v Gen 3',37,WHITE,True)
text(lcd,(30,79),'Professional mobile workstation',22,MUTED)
lcd.alpha_composite(extracted.resize((236,78),Image.Resampling.LANCZOS),(28,354))
enhfront=replace_front(front,lcd)
main=Image.new('RGBA',strict.size,'white'); put(main,enhfront,34,45)
save(main,OUT/'MAIN-ENHANCED-FRONT-CANDIDATE.png')
lcdmask=Image.new('L',main.size); ImageDraw.Draw(lcdmask).rectangle((screenpoly[0][0]+34,screenpoly[0][1]+45,screenpoly[2][0]+34-1,screenpoly[2][1]+45-1),fill=255); lcdmask.save(LAY/'MAIN-front-lcd-mask.png')
recipes['MAIN-ENHANCED-FRONT-CANDIDATE.png']={'canvas':list(main.size),'boundaryMode':'SCREEN_ONLY','sourceMethod':'ORIGINAL_PHOTO','lcdPolygon':[(x+34,y+45) for x,y in screenpoly],'windowsMode':'WINDOWS_11_PRO_LOGO_LOCKUP','windowsAsset':'layers/windows-lockup-transparent.png','windowsRectInScreen':[28,354,236,78]}

# Original 584px three-quarter photo: preserve native detail, never upscale.
angle=load(REF/'front.png')
anglebox=angle.getchannel('A').getbbox(); angle=angle.crop(anglebox)
anglepoly=[(22-anglebox[0],128-anglebox[1]),(331-anglebox[0],117-anglebox[1]),(379-anglebox[0],291-anglebox[1]),(90-anglebox[0],376-anglebox[1])]

def perspective_coeffs(dst,src):
    a=[]
    for (x,y),(u,v) in zip(dst,src):
        a.append([x,y,1,0,0,0,-u*x,-u*y,u]);a.append([0,0,0,x,y,1,-v*x,-v*y,v])
    for i in range(8):
        k=max(range(i,8),key=lambda j:abs(a[j][i]));a[i],a[k]=a[k],a[i]
        f=a[i][i]; a[i]=[z/f for z in a[i]]
        for j in range(8):
            if i!=j:
                f=a[j][i];a[j]=[v-f*w for v,w in zip(a[j],a[i])]
    return [r[-1] for r in a]

angled_lcd=ImageOps.fit(screen,(730,457)).convert('RGBA')
text(angled_lcd,(25,24),'ThinkPad P16v Gen 3',35,WHITE,True)
package=load(REF/'windows-11-pro-package.png'); package.thumbnail((70,77),Image.Resampling.LANCZOS)
coef=perspective_coeffs(anglepoly,[(0,0),(730,0),(730,457),(0,457)])
warp=angled_lcd.transform(angle.size,Image.Transform.PERSPECTIVE,coef,Image.Resampling.BICUBIC)
amask=Image.new('L',angle.size);ImageDraw.Draw(amask).polygon(anglepoly,fill=255)
warp.putalpha(ImageChops.multiply(warp.getchannel('A'),amask)); angle.alpha_composite(warp)
angle.alpha_composite(package,(112-anglebox[0],260-anglebox[1]))
angle.save(LAY/'angle-scene-master.png')
anglemain=Image.new('RGBA',(640,540),'white');put(anglemain,angle,(640-angle.width)//2,(540-angle.height)//2)
save(anglemain,OUT/'MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png')
recipes['MAIN-ENHANCED-THREE-QUARTER-CANDIDATE.png']={'canvas':list(anglemain.size),'boundaryMode':'SCREEN_ONLY','sourceMethod':'ORIGINAL_PHOTO','originalDetailPreserved':True,'lcdPolygonSource':anglepoly,'windowsMode':'WINDOWS_11_PRO_PACKAGE','windowsRectInSource':[112,260,package.width,package.height],'perspectiveCoefficients':coef,'note':'Architecture and text mapped to measured real LCD. Original fixed Windows package composited afterward, original aspect ratio, without perspective warp; corners inside LCD.'}

# PT01, hero on the approved architectural stage.
im=load(LAY/'architectural-stage.png')
text(im,(74,52),'THINKPAD P16v GEN 3  /  PROFESSIONAL WORKSTATION',25,MUTED,True)
lines(im,(74,115),['Built for','demanding ideas.'],70,WHITE,True,step=84)
lines(im,(78,346),['Engineering.','Design.','A workstation that','moves with your work.'],41,MUTED,step=57)
zone=put(im,scene_front,768,155,660)
pt(1,im,[zone,{'x':70,'y':110,'width':1100,'height':490,'label':'HEADLINE'}],[], 'High-level professional workstation purchase positioning. No Windows, full configuration grid or duplicated numerical facts. Original OEM front, original architectural scene.')

# PT02, an empty studio becomes a computer-only use context.
im=load(LAY/'natural-workspace.png')
shade=Image.new('RGBA',im.size); sd=ImageDraw.Draw(shade)
for yy in range(295): sd.line([(0,yy),(1535,yy)],fill=(9,20,33,round(140*(1-yy/295))))
im.alpha_composite(shade)
header(im,'WORKSPACE','Make room for focused work.')
text(im,(78,214),'A professional workspace, wherever your day unfolds.',34,MUTED)
zone=put(im,scene_work,630,292,700)
pt(2,im,[zone,{'x':70,'y':110,'width':1130,'height':150,'label':'HEADLINE'}],[], 'Original synthetic studio context and furniture, with the actual computer as the sole device. No people, peripherals, included software or duration claim. Different use narrative from PT01.')

# PT03, the sole complete base specification page.
im=blank(); header(im,'BASE CONFIGURATION','The configuration. Clearly.','One complete workstation. Your base specifications at a glance.')
zone=put(im,scene_front,70,327,650)
rows=[('PROCESSOR','Intel Core Ultra 7 265H'),('GRAPHICS','NVIDIA RTX PRO 2000','Blackwell Generation · 8GB GDDR7'),('MEMORY','64GB DDR5'),('INTERNAL STORAGE','1TB SSD'),('OPERATING SYSTEM','Windows 11 Pro')]
y=310
for row in rows:
    text(im,(820,y),row[0],23,BLUE,True);text(im,(820,y+32),row[1],39,WHITE,True)
    if len(row)>2: text(im,(820,y+78),row[2],25,MUTED)
    line(im,[(820,y+112),(1455,y+112)],'#31495E',1);y+=132
pt(3,im,[zone,{'x':805,'y':300,'width':650,'height':670,'label':'CONFIGURATION_TEXT'},{'x':70,'y':110,'width':1130,'height':150,'label':'HEADLINE'}],['cpu','gpu','vram','ram','ssd','os'],'Sole full base CPU/GPU/VRAM/RAM/internal SSD/OS page. ERP linked PL-1254 64GB/1TB; no alternate capacities. Product screen is original generic architecture and no repeated Windows graphic.')

# PT04, display and overall form only.
im=blank();header(im,'DISPLAY & FORM','More room for the details.')
text(im,(78,222),'16:10 workspace',48,BLUE,True)
lines(im,(78,326),['16-inch','WUXGA IPS'],70,WHITE,True,86)
lines(im,(80,550),['1920 × 1200','Anti-glare · Non-touch'],38,MUTED,step=60)
zone=put(im,scene_front,730,290,740)
pt(4,im,[zone,{'x':70,'y':110,'width':1120,'height':150,'label':'HEADLINE'},{'x':70,'y':310,'width':620,'height':370,'label':'DISPLAY_TEXT'}],['displaySize','displayResolution','displayRatio','displaySurface','displayTouch'], 'Display and form ownership only; no brightness/color-gamut assumption, keyboard detail, ports or installed capacity recap.')

# PT05, original task relationship; no repeated component/capacity table.
im=blank();header(im,'CREATIVE WORKFLOW','From concept to the next revision.','A connected sequence for design work.')
for i,(title,detail) in enumerate([('MODEL','Explore the structure'),('VISUALIZE','Inspect the composition'),('REFINE','Bring the next idea forward')]):
    x=80+i*487
    text(im,(x,315),f'0{i+1}',31,BLUE,True);text(im,(x,365),title,46,WHITE,True);text(im,(x,432),detail,28,MUTED)
    line(im,[(x,490),(x+400,490)],'#446985',2)
    if i<2: text(im,(x+415,365),'→',47,BLUE)
zone=put(im,scene_blueprint,460,510,600)
pt(5,im,[zone,{'x':70,'y':110,'width':1150,'height':150,'label':'HEADLINE'},{'x':70,'y':310,'width':1385,'height':190,'label':'WORKFLOW_TEXT'}],[], 'Generic original model/visualize/refine task relationship. No benchmark, app compatibility, included software or numerical hardware recap. Manual semantic review required for nonnumeric narrative.')

# PT06, exact original US keyboard and controls, white background.
im=blank(True);header(im,'INPUT DETAILS','Control, down to the key.',light=True)
top=load(original('CT2_06')).rotate(90,expand=True)
keyboard=top.crop((60,1010,1140,1840))
zone=put(im,keyboard,230,310,1000)
for x,label in [(80,'Backlit US keyboard'),(590,'TrackPoint + touchpad'),(1100,'Numeric keypad')]:text(im,(x,246),label,32,DARK,True)
pt(6,im,[zone,{'x':70,'y':110,'width':1100,'height':190,'label':'INPUT_TEXT'}],['keyboardLayout','keyboardBacklight','numericKeypad','trackPoint','touchpad'], 'White background and unchanged official input pixels. As-built confirms US English black backlit numeric keyboard FRU 5N21Q49827 / 5M11T54117. Source 90-degree lossless rotation and crop excludes software UI.')

# PT07, unused verified battery value, no runtime or warranty advertising.
im=blank();header(im,'BATTERY','Keep the work moving.')
text(im,(78,285),'90Wh',142,WHITE,True);text(im,(84,454),'internal battery',43,MUTED)
text(im,(82,555),'Rapid Charge',50,BLUE,True)
lines(im,(84,633),['Up to 80% in one hour*'],35,MUTED)
zone=put(im,scene_battery,780,262,660)
text(im,(80,952),'*With the supported power adapter under Lenovo test conditions. Actual charging varies.',24,MUTED)
pt(7,im,[zone,{'x':70,'y':110,'width':1120,'height':150,'label':'HEADLINE'},{'x':70,'y':280,'width':660,'height':440,'label':'BATTERY_TEXT'}],['batteryCapacity','rapidCharge'], 'Unused value: exact as-built 90Wh battery FRU 5B11M90137 plus OEM Rapid Charge capability; conditional charge claim, no runtime promise, no warranty or configuration recap. No adapter depicted.')

# PT08, physical port-detail crops. Optional front-right openings are outside crop.
im=blank(True);header(im,'PHYSICAL CONNECTIVITY','Connections, precisely placed.',light=True)
left=load(original('CT2_02')).crop((480,1020,1390,1120))
right=load(original('CT2_01')).crop((1090,1025,1575,1120))
z1=put(im,left,318,362);z2=put(im,right,525,690)
text(im,(80,291),'LEFT SIDE',29,'#49677F',True);text(im,(80,620),'RIGHT SIDE · REAR DETAIL',29,'#49677F',True)
def callout(label,tx,ty,px,py,route):
    text(im,(tx,ty),label,31,DARK,True);line(im,[(px,py),(px,route),(tx+12,route),(tx+12,ty-12)],'#4D829F',2);ImageDraw.Draw(im).ellipse((px-4,py-4,px+4,py+4),fill='#3F8AB2')
callout('HDMI 2.1',340,495,318+598-480,362+1061-1020,470)
callout('2× Thunderbolt 4',560,495,318+680-480,362+1063-1020,476)
line(im,[(318+744-480,362+1063-1020),(318+744-480,476),(572,476)],'#4D829F',2)
ImageDraw.Draw(im).ellipse((580,401,588,409),fill='#3F8AB2')
callout('USB-A',1030,495,318+816-480,362+1065-1020,460)
callout('Audio',220,860,525+1118-1090,690+1068-1025,800)
callout('SD Express 7.0',510,860,525+1227-1090,690+1066-1025,810)
callout('USB-A',840,860,525+1347-1090,690+1069-1025,820)
callout('GbE RJ-45',1130,860,525+1440-1090,690+1061-1025,830)
text(im,(80,960),'Wi-Fi + Bluetooth',30,'#49677F',True)
pt(8,im,[z1,z2,{'x':70,'y':110,'width':1120,'height':150,'label':'HEADLINE'}],['hdmi','thunderbolt','usbA','audioJack','sdReader','ethernet','wifi','bluetooth'], 'Actual official left-side and rear-right connector-detail crops. Labels terminate on real openings; two leaders point to the two Thunderbolt connectors. No generic external devices. Optional smart-card/SIM area excluded; wireless existence verified by ERP, no unverified version claim. Two USB-A shown on two sides.')

# Original red containing shape preserved; transparent margin makes the asset reusable.
logo=load(REF/'lenovo-logo-official.png'); logo.thumbnail((1536,512),Image.Resampling.LANCZOS)
transparent=Image.new('RGBA',(logo.width+20,logo.height+20));transparent.alpha_composite(logo,(10,10));transparent.save(REF/'lenovo-logo-transparent.png')
plan={'schemaVersion':3,'brand':'Lenovo','logoRole':'OEM base-product identifier','logoAssetSourceUrl':'https://media.lenovobrandworld.fiestic.com/2022/06/08010946/LenovoLogo_POS-Red-H.png','logoVisibilityMode':'ASPECT_RATIO_WORDMARK','minimumClearancePx':32,'minimumComponentSeparationPx':32,'thumbnailReviewSizePx':200,'placements':placement}
write(OUT/'logo-placement.json',plan)
sources=json.loads((WORK/'references/psref-sources.json').read_text())
for s in sources:s['sha256']=g.digest(REF/s['file']);s['authorization']='USER_CONFIRMED_CATALOG_WIDE'
write(PROD/'sources.json',sources)
facts={'schemaVersion':1,'internalId':'VL-1213','workflowPolicyVersion':'2026-10-02','currentRecordRole':'IMAGE_ONLY_VERIFIED_FACT_RECORD','identity':{'internalId':'VL-1213','oemBrand':'Lenovo','model':'ThinkPad P16v Gen 3','color':'Black'},'inputASIN':'B0HC4D4X9M','sourceMapping':{'mode':'MYSTORE_ONLY_WITH_AMAZON_INPUT','erpProductId':31213,'listingId':115154069,'linkedCurrentPhysicalConfiguration':'PL-1254','erpUrl':'https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/products/31213','mappingBasis':'Exact requested ASIN explicitly appears under VL-1213; linked current child names 64GB DDR5 and 1TB internal SSD.'},'selectedBaseConfiguration':{'id':'VL-1213-64GB-1TB','cpu':'Intel Core Ultra 7 265H','gpu':'NVIDIA RTX PRO 2000 Blackwell Generation','vram':'8GB GDDR7','ram':{'capacity':64,'unit':'GB','type':'DDR5'},'internalStorage':{'capacity':1,'unit':'TB','medium':'SSD','measurementBasis':'DECIMAL_NOMINAL'},'os':'Windows 11 Pro','basis':'Current ERP physical child PL-1254; user approved proposal naming this configuration.'},'display':{'sizeInches':16,'resolution':'1920x1200','aspectRatio':'16:10','technology':'IPS','surface':'Anti-glare','touch':False,'brightnessNits':None,'colorGamut':None},'input':{'keyboardLayout':'US English','backlit':True,'numericKeypad':True,'trackPoint':True,'touchpad':True,'oemParts':['5N21Q49827','5M11T54117']},'battery':{'capacityWh':90,'oemPart':'5B11M90137','rapidCharge':'Up to 80% in 1 hour with supported adapter; actual charging varies'},'ports':{'left':['HDMI 2.1','Thunderbolt 4','Thunderbolt 4','USB-A'],'rightStandardRear':['3.5mm combo audio','SD Express 7.0','USB-A','GbE RJ-45','Kensington Nano Security Slot'],'optionalPorts':'Not asserted; excluded from detail crop'},'sources':{'erp':'https://erp-git-feat-part-serial-numbers-overhaul-jtechdigital.vercel.app/products/31213','oem':'https://www.lenovo.com/us/en/p/LEN101T0145','psref':'https://psref.lenovo.com/Product/ThinkPad/ThinkPad_P16v_Gen_3_Intel','specification':'https://psref.lenovo.com/syspool/Sys/PDF/ThinkPad/ThinkPad_P16v_Gen_3_Intel/ThinkPad_P16v_Gen_3_Intel_Spec.pdf','asBuilt':'Private ERP-linked current-unit query inspected 2026-10-16; public receipt omits serial and private URL. Keyboards and 90Wh battery confirmed.'},'unresolvedOperationalChecks':['Marketplace/category/account publication review','Windows license and fulfillment activation','No independent brightness/gamut or optional SIM/smartcard/wireless-version claim']}
facts['selectedBaseConfiguration']['basis']='Current ERP physical child PL-1254 explicitly identifies 64GB DDR5 / 1TB SSD. Style approval is recorded separately, not used as factual evidence.'
facts['sellerPolicy']={'customized':True,'listingTitlePrefix':'MegaPC Custom','excelConfigurationScope':'BASE_ONLY','finalOperatingSystem':'Windows 11 Pro','operatingSystemPolicyStatus':'USER_CONFIRMED_CATALOG_POLICY','warrantyTemplate':g.read(REPO/'assets/warranty-disclosure-policy.json')['paragraph'],'warrantyStatus':'USER_CONFIRMED_CATALOG_POLICY','warrantyWordingConfirmation':'DIRECT_USER_INSTRUCTION_2026-10-05','imageScope':'COMPUTER_ONLY','oemWarrantyApplicabilityReview':'SELLER_MANUAL_PUBLICATION_CHECK'}
write(OUT/'product-facts.json',facts)
recipe={'version':'VL-1213-B15-BG15-v1','formFactor':'LAPTOP','boundaryMode':'SCREEN_ONLY','method':'Original authorized OEM product pixels; AI only in original scene assets; deterministic typography and identity composition','slots':recipes,'frontSourceCrop':frontbox,'angleSourceCrop':anglebox,'fonts':['Arial','Arial Bold'],'generationRecord':'generation-prompts.json','sourceLedger':'sources.json','brandOverlayPlan':'../logo-placement.json'}
write(PROD/'recipe.json',recipe)
style={'schemaVersion':1,'internalId':'VL-1213','style_approval_status':'APPROVED','approved_style_id':'B15','approved_supporting_gallery_pack':'BG15','audience_style_family':'BUSINESS_WORK','image_style_profile':'navy-technical-v1','palette':['Graphite','Cool gray','Dark navy','Icy blue'],'approval':{'quote':'批准','source':'Direct user message in this chat, after the B15/BG15 two-panel preview','date':'2026-10-16','scope':'Product-specific B15/BG15 direction; production and factual QA remain independent'},'recipeStatus':'BUILT_PENDING_VISUAL_REVIEW','recipePath':'production-v1/recipe.json','recipeSha256':g.digest(PROD/'recipe.json'),'mainBoundary':'SCREEN_ONLY','forbidden':['External devices','Accessories','Invented hardware','Unverified software entitlements','Seller warranty promotion']}
write(OUT/'style-lock.json',style)
write(PROD/'semantic-ownership.json',semantics)
write(OUT/'delivery-status.json',{'schemaVersion':1,'internalId':'VL-1213','galleryState':'AWAITING_VISUAL_REVIEW','currentQaPass':False,'deliveryScope':'FULL_GALLERY','deliveryState':'LOCAL_PRODUCTION','amazonMainEligibility':'NOT_ASSESSED'})
print('Rendered 11 slots; run finalize, inspect, then accept only if current bytes pass.')

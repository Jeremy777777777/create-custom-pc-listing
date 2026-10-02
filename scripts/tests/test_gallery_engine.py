import importlib.util, json, tempfile, unittest
from unittest.mock import patch
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('engine',Path(__file__).parents[1]/'gallery_engine.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
class Tests(unittest.TestCase):
 def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.p=Path(self.tmp.name)
 def tearDown(self): self.tmp.cleanup()
 def image(self,name,size,color='white'):
  p=self.p/name; Image.new('RGB' if p.suffix=='.jpg' else 'RGBA',size,color).save(p); return p
 def test_normalization_aspect_and_no_upscale(self):
  src=self.image('s.png',(2400,1200),'red'); out=self.p/'out.png'; g.normalize(src,out)
  im=Image.open(out); self.assertEqual(im.size,(2000,2000)); self.assertEqual(im.getpixel((1000,400))[:3],(255,255,255)); self.assertEqual(im.getpixel((1000,600))[:3],(255,0,0))
  low=self.image('low.png',(1000,1000)); before=g.digest(low)
  with self.assertRaises(ValueError): g.normalize(low,low)
  self.assertEqual(g.digest(low),before)
 def test_background_preserves_black_white_enclosed_and_red(self):
  src=self.image('ink.png',(20,20)); im=Image.open(src); pix=im.load()
  for y in range(5,15):
   for x in range(5,15): pix[x,y]=(0,0,0,255)
  pix[10,10]=(255,255,255,255); pix[8,8]=(255,0,0,255); im.save(src)
  g.remove_background(src,self.p/'clear.png'); im=Image.open(self.p/'clear.png')
  self.assertEqual(im.getpixel((0,0))[3],0)
  for pos in ((5,5),(10,10),(8,8)): self.assertEqual(im.getpixel(pos)[3],255)
  black=self.image('black.png',(20,20),'black'); im=Image.open(black); im.putpixel((10,10),(255,255,255,255)); im.save(black)
  g.remove_background(black,self.p/'white-ink.png'); im=Image.open(self.p/'white-ink.png'); self.assertEqual(im.getpixel((0,0))[3],0); self.assertEqual(im.getpixel((10,10))[3],255)
 def test_spacing_enforces_percent_and_zone(self):
  with self.assertRaises(ValueError): g.check_separation((40,100,240,300),[],(2000,2000),32)
  with self.assertRaises(ValueError): g.check_separation((100,100,300,300),[{'x':345,'y':100,'width':100,'height':100}],(2000,2000),32)
  self.assertEqual(g.check_separation((100,100,300,300),[],(2000,2000),32),50)
 def test_overlay_mask_ratio_clip_and_repeat(self):
  src=self.image('base.png',(100,100),'black'); asset=self.image('asset.png',(20,20),'red'); out=self.p/'out.png'
  with self.assertRaises(ValueError): g.overlay(src,asset,out,20,20,40,20)
  with self.assertRaises(ValueError): g.overlay(src,asset,out,20,20,20,20,'ScreenGlow')
  mask=Image.new('L',(100,100)); mask.paste(255,(20,20,40,40)); mask.save(self.p/'mask.png')
  g.overlay(src,asset,out,20,20,20,20,'ScreenGlow',18,self.p/'mask.png')
  self.assertEqual(Image.open(out).getpixel((19,19))[:3],(0,0,0))
  with self.assertRaises(ValueError): g.overlay(out,asset,out,20,20,20,20)
 def test_evidence_does_not_infer_pass_and_binds_bytes(self):
  im=self.image('PT01.png',(20,20)); evidence=self.p/'e.json'; g.write(evidence,{'schemaVersion':3,'result':'PASS','reviewer':'tester','reviewedAtUtc':'2026-10-02','images':[{'file':'PT01.png','sha256':g.digest(im),'result':'PASS','notes':'Inspected'}]})
  g.evidence(evidence,['PT01.png'],self.p); Image.new('RGBA',(20,20),'red').save(im)
  with self.assertRaises(ValueError): g.evidence(evidence,['PT01.png'],self.p)
 def test_full_validator_main_hash_and_non_destructive(self):
  for n in g.NAMES: self.image(n,(2000,2000))
  (self.p/'unbranded').mkdir()
  for n in g.PT: (self.p/'unbranded'/n).write_bytes((self.p/n).read_bytes())
  logo=self.image('logo.png',(200,100),(0,0,255,255)); im=Image.open(logo); im.putpixel((0,0),(0,0,0,0)); im.save(logo)
  # Logo asset is external to the canonical folder, as required by directory hygiene.
  external=self.p.parent/(self.p.name+'-logo.png'); external.write_bytes(logo.read_bytes()); logo.unlink(); self.addCleanup(external.unlink)
  cfg={'x':100,'y':100,'width':200,'height':100,'style':'transparent','protectedZones':[{'x':500,'y':500,'width':1000,'height':1000,'label':'PRODUCT_SILHOUETTE'}]}
  g.write(self.p/'logo-placement.json',{'brand':'OEM','placements':{n:cfg for n in g.PT},'minimumClearancePx':50,'minimumComponentSeparationPx':50})
  g.write(self.p/'logo-qa.json',{'schemaVersion':3,'generatedAtUtc':'now','brand':'OEM','logoAssetPath':'../'+external.name,'logoAssetSha256':g.digest(external),'placementPlanSha256':g.digest(self.p/'logo-placement.json'),'images':[{'file':n,'geometryGate':'PASS','commandRecord':'test fixture clean master','finalImageSha256':g.digest(self.p/n),'unbrandedSourceSha256':g.digest(self.p/'unbranded'/n)} for n in g.PT]})
  for f,names in [('visual-review.json',g.NAMES),('semantic-review.json',g.PT)]: g.write(self.p/f,{'schemaVersion':3,'result':'PASS','reviewer':'tester','reviewedAtUtc':'now','images':[{'file':n,'sha256':g.digest(self.p/n),'result':'PASS','notes':'Actual inspection'} for n in names]})
  images=g.validate(self.p,require_final=False)
  g.write(self.p/'final-image-qa.json',{'schemaVersion':3,'result':'PASS','images':images,'logoQaSha256':g.digest(self.p/'logo-qa.json'),'visualReviewSha256':g.digest(self.p/'visual-review.json'),'semanticReviewSha256':g.digest(self.p/'semantic-review.json')})
  g.validate(self.p)
  g.write(self.p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','deliveryState':'REWORK_REQUIRED','currentQaPass':False,'reason':'Legacy images','verifiedRemoteCommit':'old'})
  g.accept(self.p,'OEM'); self.assertEqual(g.read(self.p/'delivery-status.json')['galleryState'],'CURRENT_REVIEWED')
  status=g.read(self.p/'delivery-status.json'); self.assertTrue(status['currentQaPass']); self.assertEqual(status['deliveryState'],'READY_FOR_GITHUB_DELIVERY'); self.assertNotIn('verifiedRemoteCommit',status); self.assertNotEqual(status['reason'],'Legacy images')
  # Remote canonical folders can validate recorded provenance without claiming replayed source verification.
  for n in g.PT: (self.p/'unbranded'/n).unlink()
  g.validate(self.p)
  report_hash=g.digest(self.p/'final-image-qa.json'); self.image(g.MAIN[1],(2000,2000),'red')
  with self.assertRaises(ValueError): g.validate(self.p)
  self.assertEqual(g.digest(self.p/'final-image-qa.json'),report_hash)
 def test_selected_composition_and_partial_receipt_keep_legacy_bytes(self):
  for n in g.NAMES: self.image(n,(2000,2000))
  (self.p/'unbranded').mkdir(); (self.p/'unbranded'/'PT02.png').write_bytes((self.p/'PT02.png').read_bytes())
  logo=self.image('logo.png',(400,200),(0,0,0,0)); im=Image.open(logo)
  for x in range(100,300):
   for y in range(50,150): im.putpixel((x,y),(255,0,0,255))
  im.save(logo)
  cfg={'x':100,'y':100,'width':200,'height':100,'style':'transparent','protectedZones':[{'x':500,'y':500,'width':1000,'height':1000,'label':'PRODUCT_SILHOUETTE'}]}
  g.write(self.p/'logo-placement.json',{'brand':'OEM','logoRole':'OEM base-product identifier','placements':{'PT02.png':cfg},'minimumClearancePx':50,'minimumComponentSeparationPx':50})
  before={n:g.digest(self.p/n) for n in g.NAMES if n!='PT02.png'}
  g.badges(self.p,logo,self.p/'logo-placement.json',slots=['PT02.png'])
  self.assertEqual(before,{n:g.digest(self.p/n) for n in before}); self.assertEqual(g.read(self.p/'logo-qa.json')['result'],'AWAITING_VISUAL_REVIEW')
  g.write(self.p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED'})
  inventory={n:g.digest(self.p/n) for n in g.NAMES}
  for f in ['visual-review.json','semantic-review.json']:
   g.write(self.p/f,{'schemaVersion':3,'result':'PASS','reviewer':'test','reviewedAtUtc':'now','galleryInventorySha256':inventory,'images':[{'file':'PT02.png','sha256':inventory['PT02.png'],'result':'PASS','notes':'Actual selected-slot inspection'}]})
  g.accept(self.p,slots=['PT02.png']); g.validate_partial(self.p,['PT02.png'])
  self.assertEqual(g.read(self.p/'delivery-status.json')['galleryState'],'LEGACY_QUARANTINED')
  with self.assertRaises(ValueError): g.validate_partial(self.p,['PT05.png'])
  self.image('PT05.png',(2000,2000),'red')
  with self.assertRaises(ValueError): g.validate_partial(self.p,['PT02.png'])
 def test_quarantine_never_passes(self):
  g.write(self.p/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED'})
  with self.assertRaisesRegex(ValueError,'LEGACY_QUARANTINED'): g.validate(self.p)
 def test_global_policy_and_assets_revalidate_all_galleries(self):
  root=self.p; gallery=root/'product generated photo'/'VL-1234';gallery.mkdir(parents=True)
  for changed in ['references/image-spec.md','SKILL.md','README.md','assets/listing-workbook-template.xlsx','product generated photo/image-manifest-template.md']:
   self.assertEqual(g.gallery_directories(root,[changed]),[gallery])
  self.assertEqual(g.gallery_directories(root,['history/old.md']),[])
 def test_quarantine_summary_does_not_claim_full_pass(self):
  gallery=self.p/'product generated photo'/'VL-1234';gallery.mkdir(parents=True)
  (gallery/g.MAIN[0]).write_bytes(b'unchanged legacy bytes')
  g.write(gallery/'delivery-status.json',{'galleryState':'LEGACY_QUARANTINED','currentQaPass':False})
  with patch.dict('os.environ',{},clear=True): result=g.gate(self.p)
  self.assertEqual(result['fullGalleriesValidated'],0);self.assertEqual(result['quarantinedNotPassed'],1)
 def test_exact_import_exception_is_hash_and_scope_bound(self):
  root=self.p;gallery=root/'product generated photo'/'VL-1221';gallery.mkdir(parents=True)
  for n in g.NAMES:
   Image.new('RGB',(1237,937),'white').save(gallery/n)
  ref=root/'assets'/'approved.png';ref.parent.mkdir();ref.write_bytes((gallery/g.MAIN[1]).read_bytes())
  receipt={'schemaVersion':1,'internalId':'VL-1221','file':g.MAIN[1],'exceptionType':'USER_APPROVED_EXACT_ASSET_IMPORT','authorizationSource':'test explicit import','fullGalleryPass':False,'sha256':g.digest(ref),'referenceSha256':g.digest(ref),'referencePath':'assets/approved.png','dimensions':[1237,937],'mode':'RGB','unchangedCanonicalSha256':{n:g.digest(gallery/n) for n in g.NAMES if n!=g.MAIN[1]},'visualReview':{'notes':'fixture review'}}
  g.write(gallery/'approved-slot-exception.json',receipt)
  g.validate_approved_import(root,gallery,[g.MAIN[1]])
  with self.assertRaises(ValueError):g.validate_approved_import(root,gallery,[g.MAIN[1],'PT01.png'])
  Image.new('RGB',(1237,937),'red').save(gallery/'PT01.png')
  with self.assertRaises(ValueError):g.validate_approved_import(root,gallery,[g.MAIN[1]])
if __name__=='__main__': unittest.main()

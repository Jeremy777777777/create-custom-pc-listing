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
  src=self.image('s.png',(2400,1200),'red'); out=self.p/'out.png'; g.normalize(src,out,2000)
  im=Image.open(out); self.assertEqual(im.size,(2000,2000)); self.assertEqual(im.getpixel((1000,400))[:3],(255,255,255)); self.assertEqual(im.getpixel((1000,600))[:3],(255,0,0))
  low=self.image('low.png',(1000,1000)); before=g.digest(low)
  with self.assertRaises(ValueError): g.normalize(low,low,2000)
  self.assertEqual(g.digest(low),before)
 def test_amazon_pixel_boundaries_and_zoom_are_separate(self):
  for dimensions in [(500,300),(999,700),(1000,500),(1254,1254),(2400,1800),(10000,500)]:
   result=g.check_image_size(dimensions)
   self.assertEqual((result['width'],result['height']),dimensions)
   self.assertEqual(result['zoomEligibleBySize'],max(dimensions)>=1000)
  for dimensions in [(499,499),(10001,500),(0,1000)]:
   with self.assertRaises(ValueError): g.check_image_size(dimensions)
 def test_native_normalization_and_finalize_do_not_force_resize(self):
  source=self.image('native.png',(1254,937),'red'); out=self.p/'square.png'
  g.normalize(source,out)
  with Image.open(out) as image: self.assertEqual(image.size,(1254,1254))
  main=self.image(g.MAIN[0],(1254,937)); before=g.digest(main)
  with patch.object(g,'contact_sheet'):
   g.finalize(self.p,None,None,None,slots=[g.MAIN[0]])
  self.assertEqual(g.digest(main),before)
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
  for n in g.NAMES: self.image(n,(2400,1800) if n in g.MAIN else (1254,1254))
  (self.p/'unbranded').mkdir()
  for n in g.PT: (self.p/'unbranded'/n).write_bytes((self.p/n).read_bytes())
  logo=self.image('logo.png',(200,100),(0,0,255,255)); im=Image.open(logo); im.putpixel((0,0),(0,0,0,0)); im.save(logo)
  # Logo asset is external to the canonical folder, as required by directory hygiene.
  external=self.p.parent/(self.p.name+'-logo.png'); external.write_bytes(logo.read_bytes()); logo.unlink(); self.addCleanup(external.unlink)
  cfg={'x':64,'y':64,'width':126,'height':63,'style':'transparent','protectedZones':[{'x':300,'y':300,'width':700,'height':700,'label':'PRODUCT_SILHOUETTE'}]}
  g.write(self.p/'logo-placement.json',{'brand':'OEM','placements':{n:cfg for n in g.PT},'minimumClearancePx':50,'minimumComponentSeparationPx':50})
  g.write(self.p/'logo-qa.json',{'schemaVersion':3,'generatedAtUtc':'now','brand':'OEM','logoAssetPath':'../'+external.name,'logoAssetSha256':g.digest(external),'placementPlanSha256':g.digest(self.p/'logo-placement.json'),'images':[{'file':n,'geometryGate':'PASS','commandRecord':'test fixture clean master','finalImageSha256':g.digest(self.p/n),'unbrandedSourceSha256':g.digest(self.p/'unbranded'/n)} for n in g.PT]})
  for f,names in [('visual-review.json',g.NAMES),('semantic-review.json',g.PT)]: g.write(self.p/f,{'schemaVersion':3,'result':'PASS','reviewer':'tester','reviewedAtUtc':'now','images':[{'file':n,'sha256':g.digest(self.p/n),'result':'PASS','notes':'Actual inspection'} for n in names]})
  images=g.validate(self.p,require_final=False)
  self.assertEqual((images[0]['width'],images[0]['height']),(2400,1800))
  self.assertEqual((images[3]['width'],images[3]['height']),(1254,1254))
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
  for n in g.NAMES: self.image(n,(1254,1254))
  (self.p/'unbranded').mkdir(); (self.p/'unbranded'/'PT02.png').write_bytes((self.p/'PT02.png').read_bytes())
  logo=self.image('logo.png',(400,200),(0,0,0,0)); im=Image.open(logo)
  for x in range(100,300):
   for y in range(50,150): im.putpixel((x,y),(255,0,0,255))
  im.save(logo)
  cfg={'x':64,'y':64,'width':126,'height':63,'style':'transparent','protectedZones':[{'x':300,'y':300,'width':700,'height':700,'label':'PRODUCT_SILHOUETTE'}]}
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
 def test_ai_effect_import_is_scoped_and_never_full_qa(self):
  root=self.p; gallery=root/'product generated photo'/'VL-1326'; source=gallery/'ai-gallery-silver-blue-20261005'; source.mkdir(parents=True)
  for n in g.NAMES: Image.new('RGB',(1254,1254),'white').save(gallery/n)
  for n in g.PT: (source/n).write_bytes((gallery/n).read_bytes())
  hashes={n:g.digest(gallery/n) for n in g.PT}
  g.write(source/'native-file-checks.json',{'files':[{'file':n,'sha256':hashes[n]} for n in g.PT]})
  g.write(source/'approval-and-review.json',{'strictGalleryQaPass':False})
  receipt={'schemaVersion':1,'internalId':'VL-1326','exceptionType':'USER_APPROVED_AI_EFFECT_IMPORT','authorization':{'aiMethodQuote':'explicit method approval','replacementQuote':'explicit byte replacement','sizePolicyQuote':'explicit size rule change'},'fullGalleryPass':False,'publicationReadiness':'NOT_ASSESSED','limitations':['AI approximation'],'sourceReviewSha256':g.digest(source/'approval-and-review.json'),'sourceFileChecksSha256':g.digest(source/'native-file-checks.json'),'images':hashes,'unchangedMainSha256':{n:g.digest(gallery/n) for n in g.MAIN}}
  g.write(gallery/'approved-ai-effect-import.json',receipt)
  g.validate_ai_effect_import(root,gallery,g.PT)
  with self.assertRaises(ValueError): g.validate_ai_effect_import(root,gallery,[g.PT[0]])
  receipt['fullGalleryPass']=True; g.write(gallery/'approved-ai-effect-import.json',receipt)
  with self.assertRaises(ValueError): g.validate_ai_effect_import(root,gallery,g.PT)
  receipt['fullGalleryPass']=False; g.write(gallery/'approved-ai-effect-import.json',receipt)
  Image.new('RGB',(1254,1254),'red').save(gallery/g.PT[0])
  with self.assertRaises(ValueError): g.validate_ai_effect_import(root,gallery,g.PT)
  (gallery/g.PT[0]).write_bytes((source/g.PT[0]).read_bytes())
  Image.new('RGB',(1254,1254),'red').save(gallery/g.MAIN[0])
  with self.assertRaises(ValueError): g.validate_ai_effect_import(root,gallery,g.PT)
 def test_vl1276_eleven_ai_import_frozen_bytes_and_no_qa(self):
  import shutil
  root=self.p; product=root/'product generated photo'/'VL-1276'; product.mkdir(parents=True)
  original=Path(__file__).parents[2]/'product generated photo'/'VL-1276'
  source=product/'ai-gallery-architectural-20261005'
  shutil.copytree(original/'ai-gallery-architectural-20261005',source)
  for n in g.NAMES: shutil.copyfile(source/n,product/n)
  shutil.copyfile(original/'approved-ai-gallery-import.json',product/'approved-ai-gallery-import.json')
  shutil.copyfile(original/'delivery-status.json',product/'delivery-status.json')
  g.validate_vl1276_ai_gallery_import(root,product,g.NAMES)
  with self.assertRaises(ValueError): g.validate_vl1276_ai_gallery_import(root,product,g.PT)
  with self.assertRaises(ValueError): g.validate_vl1276_ai_gallery_import(root,product.with_name('VL-9999'),g.NAMES)
  receipt=g.read(product/'approved-ai-gallery-import.json')
  receipt['fullGalleryPass']=True; g.write(product/'approved-ai-gallery-import.json',receipt)
  with self.assertRaises(ValueError): g.validate_vl1276_ai_gallery_import(root,product,g.NAMES)
  receipt['fullGalleryPass']=False; g.write(product/'approved-ai-gallery-import.json',receipt)
  Image.new('RGB',(1254,1254),'red').save(product/g.MAIN[0])
  with self.assertRaises(ValueError): g.validate_vl1276_ai_gallery_import(root,product,g.NAMES)
  shutil.copyfile(source/g.MAIN[0],product/g.MAIN[0])
  receipt['images'][g.MAIN[0]]='0'*64; g.write(product/'approved-ai-gallery-import.json',receipt)
  with self.assertRaises(ValueError): g.validate_vl1276_ai_gallery_import(root,product,g.NAMES)
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

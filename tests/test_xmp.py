import xml.etree.ElementTree as ET
from src.models import LightroomSettings
from src.xmp_utils import generate_xmp

def test_generate_xmp_from_scratch():
    settings = LightroomSettings(
        exposure=0.5,
        contrast=20,
        color_temp=5500,
        tint=10
    )
    
    xmp_str = generate_xmp(settings)
    
    assert 'xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"' in xmp_str
    assert 'crs:Exposure2012="0.5"' in xmp_str
    assert 'crs:Contrast2012="20"' in xmp_str
    assert 'crs:Temperature="5500"' in xmp_str
    assert 'crs:Tint="10"' in xmp_str

def test_generate_xmp_with_existing_content():
    settings = LightroomSettings(
        exposure=-0.5,
        highlights=-50
    )
    
    existing_xmp = '''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
   crs:Version="15.0"
   crs:Exposure2012="0.0"
   crs:Contrast2012="10">
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''
    
    xmp_str = generate_xmp(settings, existing_xmp)
    
    assert 'crs:Exposure2012="-0.5"' in xmp_str
    assert 'crs:Highlights2012="-50"' in xmp_str
    assert 'crs:Contrast2012="10"' in xmp_str  # Maintained from original

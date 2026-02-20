import xml.etree.ElementTree as ET
from typing import Optional
from .models import LightroomSettings

# Namespace mapping for Lightroom XMP
XMP_NS = {
    'x': 'adobe:ns:meta/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'crs': 'http://ns.adobe.com/camera-raw-settings/1.0/'
}

for prefix, uri in XMP_NS.items():
    ET.register_namespace(prefix, uri)

def generate_xmp(settings: LightroomSettings, original_xmp_content: Optional[str] = None) -> str:
    """
    Generates a new XMP string based on the given Lightroom settings.
    If original_xmp_content is provided, it attempts to modify it.
    Otherwise, creates a basic valid XMP structure.
    """
    if original_xmp_content:
        try:
            # Parse the existing XMP and update the crs attributes
            root = ET.fromstring(original_xmp_content)
            # Find the rdf:Description element which usually holds the crs namespace attributes
            description_xpath = ".//rdf:Description"
            desc_elem = root.find(description_xpath, XMP_NS)
            
            if desc_elem is not None:
                _apply_settings_to_element(desc_elem, settings)
                return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            # Fallback to generating a new one if parsing fails
            pass

    # Bare minimum valid XMP structure for Lightroom
    xmp_meta = ET.Element(f"{{{XMP_NS['x']}}}xmpmeta", {"x:xmptk": "Adobe XMP Core (lightroom-gemini)"})
    rdf_rdf = ET.SubElement(xmp_meta, f"{{{XMP_NS['rdf']}}}RDF")
    rdf_desc = ET.SubElement(rdf_rdf, f"{{{XMP_NS['rdf']}}}Description", {
        f"{{{XMP_NS['rdf']}}}about": "",
        f"{{{XMP_NS['crs']}}}Version": "15.0",
        f"{{{XMP_NS['crs']}}}ProcessVersion": "15",
        f"{{{XMP_NS['crs']}}}HasSettings": "True"
    })
    
    _apply_settings_to_element(rdf_desc, settings)
    
    # Prepend xml declaration and return
    xmp_str = '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
    xmp_str += ET.tostring(xmp_meta, encoding='unicode')
    xmp_str += '\n<?xpacket end="w"?>'
    return xmp_str

def _apply_settings_to_element(element: ET.Element, settings: LightroomSettings):
    """
    Applies the settings to the given XML element as namespaced attributes.
    """
    mapping = {
        "exposure": "Exposure2012",
        "contrast": "Contrast2012",
        "highlights": "Highlights2012",
        "shadows": "Shadows2012",
        "whites": "Whites2012",
        "blacks": "Blacks2012",
        "texture": "Texture",
        "clarity": "Clarity2012",
        "dehaze": "Dehaze",
        "vibrance": "Vibrance",
        "saturation": "Saturation",
        "color_temp": "Temperature",
        "tint": "Tint",
    }
    
    for field, crs_attr in mapping.items():
        val = getattr(settings, field)
        if val is not None:
            # Add or update the attribute in the crs namespace
            attr_qname = f"{{{XMP_NS['crs']}}}{crs_attr}"
            element.set(attr_qname, str(val))

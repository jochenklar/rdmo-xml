import sys
from io import BytesIO
from xml.dom.minidom import parseString
from xml.sax.saxutils import XMLGenerator

xml_ns = {
    'xmlns:dc': 'http://purl.org/dc/elements/1.1/'
}

uri_prefix = 'https://rdmo.jochenklar.dev/terms'

options = {
        'relation_type/is_cited_by': 'IsCitedBy',
        'relation_type/cites': 'Cites',
        'relation_type/is_supplement_to': 'IsSupplementTo',
        'relation_type/is_supplemented_by': 'IsSupplementedBy',
        'relation_type/is_continued_by': 'IsContinuedBy',
        'relation_type/continues': 'Continues',
        'relation_type/describes': 'Describes',
        'relation_type/is_described_by': 'IsDescribedBy',
        'relation_type/has_metadata': 'HasMetadata',
        'relation_type/is_metadata_for': 'IsMetadataFor',
        'relation_type/has_version': 'HasVersion',
        'relation_type/is_version_of': 'IsVersionOf',
        'relation_type/is_new_version_of': 'IsNewVersionOf',
        'relation_type/is_previous_version_of': 'IsPreviousVersionOf',
        'relation_type/is_part_of': 'IsPartOf',
        'relation_type/has_part': 'HasPart',
        'relation_type/is_published_in': 'IsPublishedIn',
        'relation_type/is_referenced_by': 'IsReferencedBy',
        'relation_type/references': 'References',
        'relation_type/is_documented_by': 'IsDocumentedBy',
        'relation_type/documents': 'Documents',
        'relation_type/is_compiled_by': 'IsCompiledBy',
        'relation_type/Compiles': 'Compiles',
        'relation_type/is_variant_form_of': 'IsVariantFormOf',
        'relation_type/is_original_form_of': 'IsOriginalFormOf',
        'relation_type/is_identical_to': 'IsIdenticalTo',
        'relation_type/is_reviewed_by': 'IsReviewedBy',
        'relation_type/reviews': 'Reviews',
        'relation_type/is_derived_from': 'IsDerivedFrom',
        'relation_type/is_source_of': 'IsSourceOf',
        'relation_type/is_required_by': 'IsRequiredBy',
        'relation_type/requires': 'Requires',
        'relation_type/obsoletes': 'Obsoletes',
        'relation_type/is_obsoleted_by': 'IsObsoletedBy'
    }

optionset_key = options.keys()[0].split('/')[0]
optionset_uri = '{}/options/{}'.format(uri_prefix, optionset_key)

stream = BytesIO()

xml = XMLGenerator(stream, encoding='utf-8')
xml.startDocument()
xml.startElement('rdmo', xml_ns)

xml.startElement('optionset', {
    'dc:uri': optionset_uri
})
xml.startElement('uri_prefix', {})
xml.characters(uri_prefix)
xml.endElement('uri_prefix')

xml.startElement('key', {})
xml.characters(optionset_key)
xml.endElement('key')

xml.endElement('optionset')

for order, option in enumerate(options.items()):
    option_path, option_text = option
    option_key = option_path.replace(optionset_key + '/', '')
    option_uri = '{}/options/{}'.format(uri_prefix, option_path)

    xml.startElement('option', {
        'dc:uri': option_uri
    })
    xml.startElement('uri_prefix', {})
    xml.characters(uri_prefix)
    xml.endElement('uri_prefix')

    xml.startElement('key', {})
    xml.characters(option_key)
    xml.endElement('key')

    xml.startElement('optionset', {
        'dc:uri': optionset_uri
    })
    xml.endElement('optionset')

    xml.startElement('order', {})
    xml.characters(str(order))
    xml.endElement('order')

    xml.startElement('text', {
        'lang': 'en'
    })
    xml.characters(option_text)
    xml.endElement('text')

    xml.startElement('text', {
        'lang': 'de'
    })
    xml.characters(option_text)
    xml.endElement('text')

    xml.endElement('option')

xml.endElement('rdmo')
xml.endDocument()

xml_string = stream.getvalue()

dom = parseString(xml_string)
pretty_xml_string = dom.toprettyxml()
sys.stdout.write(pretty_xml_string)

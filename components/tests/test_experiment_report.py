def test_gallery_escapes_identifiers_and_discloses_missing_examples():
    from component_inspector.evaluation.reports import gallery_html
    text=gallery_html({'TP':{'id':'<script>alert(1)</script>','original':'gallery/TP_original.png',
        'overlay':'gallery/TP_overlay.png','mask':None},'FN':{'status':'no_decodable_example'}},'example')
    assert '<script>' not in text
    assert '&lt;script&gt;' in text
    assert 'no example' in text
    assert 'not probability' in text

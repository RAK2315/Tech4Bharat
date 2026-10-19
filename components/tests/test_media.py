"""Actual byte decoding and warnings must not become fake normal decisions."""
import importlib
import importlib.util
import io
from PIL import Image
import pytest


def api():
    name='component_inspector.vision.media'
    assert importlib.util.find_spec(name), 'media validation not implemented'
    return importlib.import_module(name)


def encoded(format='PNG',size=(128,128)):
    stream=io.BytesIO();Image.new('RGB',size,0).save(stream,format=format);return stream.getvalue()


def test_dark_blurry_image_is_decoded_with_warnings_not_rejected():
    result=api().decode_media(encoded())
    assert result.image.size==(128,128)
    assert {'low_exposure','low_focus'}<=set(result.warnings)
    assert result.image.info=={}


@pytest.mark.parametrize('data,code',[(b'not a png',422),(b'x'*(10*1024**2+1),413)],
                         ids=['invalid_bytes','encoded_overflow'])
def test_bad_bytes_and_encoded_overflow_have_specific_rejections(data,code):
    module=api()
    with pytest.raises(module.MediaError) as error:module.decode_media(data)
    assert error.value.status_code==code


def test_gif_and_too_small_images_are_not_scored_as_normal():
    module=api()
    for data,code in [(encoded('GIF'),415),(encoded(size=(127,128)),422)]:
        with pytest.raises(module.MediaError) as error:module.decode_media(data)
        assert error.value.status_code==code

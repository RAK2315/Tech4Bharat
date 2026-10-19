"""Bound actual JPEG/PNG decoding; image quality diagnostics are warnings only."""
from dataclasses import dataclass
import io
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
from scipy.ndimage import laplace


class MediaError(ValueError):
    def __init__(self, message, status_code):
        super().__init__(message);self.status_code=status_code


@dataclass(frozen=True)
class DecodedMedia:
    image: object
    warnings: list[str]
    diagnostics: dict


def decode_media(data):
    if not data or len(data)>10*1024**2:
        raise MediaError('Encoded image empty or above 10 MiB limit',413)
    try:
        with Image.open(io.BytesIO(data)) as source:
            if source.format not in ('JPEG','PNG'):
                raise MediaError('Only JPEG/PNG images supported',415)
            if source.width*source.height>20_000_000:
                raise MediaError('Decoded image above 20 MP limit',413)
            if getattr(source,'n_frames',1)!=1:
                raise MediaError('Animated/multipage images unsupported',415)
            if min(source.size)<128:
                raise MediaError('Image minimum side below 128 pixels',422)
            image=ImageOps.exif_transpose(source).convert('RGB');image.load()
            image.info.clear()
    except Image.DecompressionBombError as exc:
        raise MediaError('Decoded image exceeds safe limits',413) from exc
    except (UnidentifiedImageError,OSError) as exc:
        raise MediaError('Actual image decode failed',422) from exc
    gray=np.asarray(image.convert('L').resize((256,256),Image.Resampling.BILINEAR),dtype=np.float32)
    mean=float(gray.mean()/255);clipped=float(((gray<2.55)|(gray>252.45)).mean())
    focus=float(laplace(gray).var())
    warnings=[]
    if mean<.05:warnings.append('low_exposure')
    if mean>.95:warnings.append('high_exposure')
    if clipped>.5:warnings.append('high_clipping')
    if focus<20:warnings.append('low_focus')
    return DecodedMedia(image,warnings,{'mean_luma':mean,'clipped_fraction':clipped,
        'focus_laplacian_variance':focus,'warning_status':'provisional_not_validated_retake_rule'})

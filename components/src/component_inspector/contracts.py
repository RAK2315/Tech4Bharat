"""Shared records retain source identity separately from experimental access."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ImageRecord:
    dataset: str
    release_hash: str
    recipe: str
    id: str
    path: str
    mask_path: str | None
    official_split: str
    label: int | None
    defect_type: str | None = None
    group: str | None = None
    physical_group: str | None = None
    grouping_confidence: str = 'physical_identity_unknown'
    hashes: dict = field(default_factory=dict)
    original_shape: tuple | None = None
    experiment_role: str | None = None
    quarantine_reason: str | None = None
    provenance: dict = field(default_factory=dict)
    parent_id: str | None = None


@dataclass(frozen=True)
class AuditReport:
    records: list[ImageRecord]
    summary: dict
    duplicate_pairs: list[dict]


@dataclass(frozen=True)
class SplitManifest:
    records: list[ImageRecord]
    fit_ids: list[str]
    reference_ids: list[str]
    membership_hash: str


@dataclass(frozen=True)
class PreparedImage:
    rgb_float32: object
    valid_roi: object
    geometry: dict
    original_shape: tuple

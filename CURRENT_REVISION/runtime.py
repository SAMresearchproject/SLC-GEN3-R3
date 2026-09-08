"""Portable release binding; upstream arithmetic and checkpoint code is unchanged."""
from functools import lru_cache
from importlib import import_module
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
GENERATION = "SLC-GEN2-R4-RESEARCH-20260907-1"

def current_generation():
    return GENERATION

def require_generation(generation):
    if generation != GENERATION:
        raise ValueError("This session belongs to another release generation")

def record(name):
    if name.upper() != "SLC":
        raise ValueError("This standalone repository exports the SLC engine; CE domain deployments are separate")
    return {"name": "SLC", "version": "SLC-GEN2-R4", "generation": GENERATION}

def verify_sources():
    manifest = json.loads((ROOT / "provenance/SOURCE_MANIFEST.json").read_text())
    for row in manifest["files"]:
        path = (ROOT / row["path"]).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError("Source manifest path escapes the release")
        if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("Exported upstream source differs: " + row["path"])
    return {"verified_files": len(manifest["files"]), "generation": GENERATION}

@lru_cache(maxsize=1)
def load_slc():
    verify_sources()
    return import_module("CURRENT_REVISION.engines.SLC.gen2_runtime")

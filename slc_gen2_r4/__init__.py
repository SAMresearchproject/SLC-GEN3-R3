"""Research-only SLC-GEN2-R4. See LICENSE.md for the permission grant."""
from CURRENT_REVISION.runtime import load_slc, current_generation, verify_sources

__version__ = "4.0.0"
DEPLOYMENT_OPERATIONS = {
    "GEN2_SOURCE_BATCH": "the SAM multi-host CPU/GPU/T500 deployment",
    "GEN2_TAU_ASSIGNMENT": "the separately installed tau application",
    "GEN2_TAU_REPLAY": "the separately installed tau application",
    "GEN2_TAU_FEATURE_CATALOG": "the separately installed tau application",
}

class Runtime:
    """Context manager returning upstream exact results without changing their schemas."""
    def __enter__(self):
        self._runtime = load_slc().open_runtime()
        self._runtime.__enter__()
        return self

    def __exit__(self, *args):
        return self._runtime.__exit__(*args)

    def execute(self, operation, payload):
        if operation in DEPLOYMENT_OPERATIONS:
            raise ValueError(operation + " requires " + DEPLOYMENT_OPERATIONS[operation]
                             + "; see docs/DISTRIBUTION_SCOPE.md")
        return self._runtime.execute(operation, payload)

    def compose(self, left_checkpoint, right_checkpoint):
        from CURRENT_REVISION.engines.SLC.gen2.history_summary import compose
        return compose(left_checkpoint, right_checkpoint, self._runtime.exact_information())

def open_runtime():
    return Runtime()

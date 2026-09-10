"""Typed errors raised by the SAM Language v0.6.0 candidate."""


class SamLanguageError(Exception):
    """Base class for SAM Language errors."""


class ParseError(SamLanguageError):
    """Source text could not be parsed."""


class RawProgramExecutionError(SamLanguageError):
    """A raw parsed program was sent directly to execution."""


class NameResolutionError(SamLanguageError):
    """A symbol, entity, or operator could not be resolved."""


class UnknownEntityError(NameResolutionError):
    """An entity identifier or alias is not registered."""


class UnknownOperatorError(NameResolutionError):
    """An operator identifier is not registered."""


class CLIUsageError(SamLanguageError):
    """The requested CLI operation or argument form is invalid."""


class ContractValidationError(SamLanguageError):
    """A source contract or manifest failed validation."""


class InternalCLIError(SamLanguageError):
    """An unexpected internal CLI failure was translated into a typed diagnostic."""


class TypeCheckError(SamLanguageError):
    """A program violates a typed operator signature."""


class ContextRoleError(SamLanguageError):
    """A contextual role is missing or unsupported."""


class AuthorityError(SamLanguageError):
    """An authority boundary, OPEN edge, or status gate was violated."""


class ProvenanceError(SamLanguageError):
    """A provenance assertion is invalid."""


class ProvenanceCycleError(ProvenanceError):
    """A provenance dependency cycle was found."""

    def __init__(self, cycle_path):
        self.cycle_path = list(cycle_path)
        super().__init__("Provenance dependency cycle: " + " -> ".join(self.cycle_path))


class QPError(SamLanguageError):
    """Base class for directly integrated structural QP grammar errors."""


class QPDomainError(TypeCheckError, QPError):
    """A typed QP constructor input is outside its frozen finite domain."""


class QPMultiplicityError(AuthorityError, QPError):
    """A program-scoped QP multiplicity constraint was violated."""


class QPRegistrationError(NameResolutionError, QPError):
    """A QP grammar source or registered production could not be resolved."""


class SLCError(SamLanguageError):
    """Base class for the exact formal SLC C1 simulator."""


class SLCFormalProfileRequired(AuthorityError, SLCError):
    """A formal SLC operator was requested outside its isolated profile."""


class SLCRegisterArityError(TypeCheckError, SLCError):
    """An SLC state does not have the frozen twelve-lebit arity."""


class SLCSiteRangeError(TypeCheckError, SLCError):
    """An SLC site is outside L0 through L11."""


class SLCControlTargetAliasError(TypeCheckError, SLCError):
    """An ordered response aliases its control and target sites."""


class SLCStateInvariantError(TypeCheckError, SLCError):
    """An exact SLC state violates canonical form or normalization."""


class SLCStateCustodyError(AuthorityError, SLCError):
    """An SLC state or route receipt failed deterministic custody."""


class SLCUnsupportedPhaseError(AuthorityError, SLCError):
    """Complex phase is outside the frozen real C1 kernel."""


class SLCUnsupportedPublicationError(AuthorityError, SLCError):
    """Publication or Born sampling is not installed in the C1 kernel."""


class SLCUnsupportedConnectivityError(AuthorityError, SLCError):
    """Formal placement was incorrectly promoted to physical connectivity."""

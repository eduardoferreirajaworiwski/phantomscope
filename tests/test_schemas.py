from pydantic import ValidationError

from phantomscope.models.schemas import DataOrigin, DomainInfrastructure, TargetRequest, TargetType


def test_target_request_sanitizes_input() -> None:
    request = TargetRequest(target="  Acme[.]Com  ", target_type=TargetType.DOMAIN)
    assert request.target == "acme.com"


def test_infrastructure_defaults_include_origin_metadata() -> None:
    infrastructure = DomainInfrastructure()
    assert infrastructure.origin == DataOrigin.LIVE
    assert infrastructure.source == "composite-enrichment"


def test_target_request_rejects_empty_after_sanitization() -> None:
    try:
        TargetRequest(target="!!!", target_type=TargetType.BRAND)
    except ValidationError:
        pass
    else:
        raise AssertionError("expected validation error for empty sanitized target")

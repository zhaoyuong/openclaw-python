"""Unit tests for agent abort signal"""
import pytest
from openclaw.agents.abort import AbortController, AbortError, AbortSignal


def test_abort_signal_not_aborted_initially():
    signal = AbortSignal()
    assert not signal.aborted
    assert signal.reason is None


def test_abort_controller_abort():
    controller = AbortController()
    assert not controller.signal.aborted
    controller.abort()
    assert controller.signal.aborted
    with pytest.raises(AbortError):
        controller.signal.throw_if_aborted()


def test_abort_with_reason():
    controller = AbortController()
    exc = ValueError("test")
    controller.abort(exc)
    assert controller.signal.reason is exc
    with pytest.raises(ValueError):
        controller.signal.throw_if_aborted()

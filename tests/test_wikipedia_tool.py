"""Unit tests for the structured `wikipedia_tool` implementation.

These tests mock the `wikipedia` package to avoid network calls and verify
the structured JSON output and disambiguation handling.
"""

import json

import pytest

from src.tools import wikipedia_tool


def test_wikipedia_tool_success(monkeypatch):
    """When search and summary succeed, tool returns success and summary."""

    def fake_search(q):
        return ["Apple Inc."]

    def fake_summary(title, sentences=8, auto_suggest=False, redirect=True):
        return "Apple Inc. is an American multinational technology company. The company's CEO is Tim Cook."

    monkeypatch.setattr("wikipedia.search", fake_search)
    monkeypatch.setattr("wikipedia.summary", fake_summary)

    # Invoke the tool via its tool wrapper interface
    raw = wikipedia_tool.invoke({"query": "Who is Apple's CEO?"})
    data = json.loads(raw)

    assert data["success"] is True
    assert data["query"] == "Who is Apple's CEO?"
    assert data["title"] == "Apple Inc."
    assert "Tim Cook" in data["summary"]


def test_wikipedia_tool_disambiguation(monkeypatch):
    """When summary raises DisambiguationError, candidates are returned."""

    from wikipedia import DisambiguationError

    def fake_search(q):
        return ["Apple"]

    def fake_summary(title, sentences=8, auto_suggest=False, redirect=True):
        raise DisambiguationError(title, ["Apple (fruit)", "Apple Inc."])

    monkeypatch.setattr("wikipedia.search", fake_search)
    monkeypatch.setattr("wikipedia.summary", fake_summary)

    raw = wikipedia_tool.invoke({"query": "Apple"})
    data = json.loads(raw)

    assert data["success"] is False
    assert data["title"] == "Apple"
    assert isinstance(data["candidates"], list)
    assert "Apple Inc." in data["candidates"]

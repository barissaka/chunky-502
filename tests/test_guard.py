"""Tests for the decline path (src/chunky/guard.py).

Added by barissaka for CHUNKY-130 (US-06 Decline when the assistant does not know),
sub-tasks CHUNKY-181 (out-of-scope reply), CHUNKY-182 (individual-case rule) and
CHUNKY-183 (tests).

These tests call no model and need no index, Google Cloud login or network; they run in
about a second. They check the code that recognises the two fixed sentences, and that the
answer prompt in use still contains both sentences word for word. Whether the model
itself declines the right questions is measured in notebooks/06_decline_check.ipynb
(test cases TC-06-2 and TC-06-3), because that needs the model.

Run from the repository root:  python -m pytest
"""

from pathlib import Path

import pytest
import yaml

from chunky.guard import (
    ADVICE_NOTICE,
    DECLINE_REPLY,
    find_advice_phrases,
    has_advice_notice,
    is_decline,
)

ROOT = Path(__file__).resolve().parents[1]


def _prompt_in_use():
    """Read the answer prompt named in config/rag.yaml.

    Returns:
        tuple[str, str]: the prompt name (for example "answer_v3") and the prompt text.
    """
    cfg = yaml.safe_load((ROOT / "config" / "rag.yaml").read_text(encoding="utf-8"))
    name = cfg["generation"]["prompt"]
    return name, (ROOT / "prompts" / f"{name}.txt").read_text(encoding="utf-8")


# --- CHUNKY-181: out-of-scope reply ---------------------------------------------------
@pytest.mark.parametrize(
    "reply",
    [
        DECLINE_REPLY,
        DECLINE_REPLY.rstrip("."),  # final period left out
        f"**{DECLINE_REPLY}**",  # Markdown bold
        f'"{DECLINE_REPLY}"',  # in quotes
        f"\n  {DECLINE_REPLY}\n",  # surrounding blank lines and spaces
        DECLINE_REPLY.replace("altı mevzuat", "altı\nmevzuat"),  # line break inside the sentence
        "BU KONU, ASİSTANIN KULLANDIĞI ALTI MEVZUAT METNİNDE YER ALMIYOR.",  # Turkish upper case
        DECLINE_REPLY + " Yine de genel olarak şunu söyleyebilirim: ...",  # text after the sentence
    ],
)
def test_is_decline_recognises_the_fixed_reply(reply):
    """The fixed reply is recognised whatever the model wraps around it."""
    assert is_decline(reply) is True


@pytest.mark.parametrize(
    "reply",
    [
        None,
        "",
        "Kırmızı ışıkta geçmenin cezası 5.000 Türk lirasıdır. [KTK-m47]",  # ordinary answer
        "Bu konu Karayolları Trafik Kanunu'nun 47. maddesinde düzenlenmiştir. [KTK-m47]",  # same first words
        "Hız sınırı 50 km/saattir. [KTK-m50] " + DECLINE_REPLY,  # sentence only at the end of an answer
    ],
)
def test_is_decline_leaves_other_replies(reply):
    """An empty reply, an ordinary answer, or an answer that only ends with the sentence is not a decline."""
    assert is_decline(reply) is False


# --- CHUNKY-182: individual-case rule -------------------------------------------------
@pytest.mark.parametrize(
    "answer",
    [
        f"İtiraz sulh ceza hâkimliğine yapılır. [KTY-m160]\n\n{ADVICE_NOTICE}",
        f"İtiraz sulh ceza hâkimliğine yapılır. [KTY-m160]\n\n*{ADVICE_NOTICE.rstrip('.')}*",  # italics, no period
        "İtiraz süresi vardır. [KTY-m160] " + ADVICE_NOTICE.replace("; ", ";\n"),  # line break inside the notice
    ],
)
def test_has_advice_notice_finds_the_notice(answer):
    """The no-advice notice is found at the end of an answer."""
    assert has_advice_notice(answer) is True


@pytest.mark.parametrize(
    "answer",
    [None, "", "Kırmızı ışıkta geçmenin cezası 5.000 Türk lirasıdır. [KTK-m47]", DECLINE_REPLY],
)
def test_has_advice_notice_is_false_without_the_notice(answer):
    """An empty answer, an ordinary answer and the decline reply carry no notice."""
    assert has_advice_notice(answer) is False


def test_find_advice_phrases_flags_advising_wording():
    """Wording that tells the user what to do is listed."""
    found = find_advice_phrases("Bence itiraz etmelisiniz; kazanma şansınız yüksek.")
    assert found == ["bence", "itiraz etmelisiniz", "kazanma şansınız"]


def test_find_advice_phrases_ignores_the_notice_itself():
    """The notice contains the word "tavsiye" but is not advice."""
    assert find_advice_phrases(f"İtiraz sulh ceza hâkimliğine yapılır. [KTY-m160]\n\n{ADVICE_NOTICE}") == []
    assert find_advice_phrases(None) == []


# --- the prompt and the code must hold the same two sentences --------------------------
def test_prompt_in_use_contains_the_decline_reply():
    """If the sentence is edited in the prompt or in guard.py only, declines are no longer recognised."""
    name, text = _prompt_in_use()
    assert DECLINE_REPLY in text, f"prompts/{name}.txt does not contain DECLINE_REPLY word for word"


def test_prompt_in_use_contains_the_advice_notice():
    """The same for the no-advice notice."""
    name, text = _prompt_in_use()
    assert ADVICE_NOTICE in text, f"prompts/{name}.txt does not contain ADVICE_NOTICE word for word"

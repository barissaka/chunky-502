"""Decline path: the fixed reply for questions outside the six texts.

Added by barissaka for CHUNKY-130 (US-06 Decline when the assistant does not know),
sub-tasks CHUNKY-181 (out-of-scope reply) and CHUNKY-182 (individual-case rule).

The answer prompt (prompts/answer_v2.txt and later) tells the model to reply with exactly
DECLINE_REPLY when the retrieved articles do not answer the question. This module holds
that sentence and recognises it in the model's reply, so that answer.py can mark the
result as declined and return the sentence unchanged.

Why the model decides and not a score threshold: on 23 Nov 2026 the retrieval scores of
in-scope and out-of-scope questions overlapped (notebooks/06_decline_check.ipynb), so no
threshold separated them. A threshold on reranker scores is to be measured once the
reranker is in the pipeline.
"""

import re

# The one sentence shown to the user when the texts do not cover the question.
# The answer prompt in use must contain it word for word (checked by tests/test_guard.py).
DECLINE_REPLY = "Bu konu, asistanın kullandığı altı mevzuat metninde yer almıyor."

# Characters a model may put around the sentence: quotes, Markdown emphasis, spaces, final period.
_WRAPPING = " \t\r\n\"'“”‘’«»*_`."


def _normalize(text):
    """Lower-case the text and reduce every run of whitespace to one space.

    Args:
        text (str): any text.

    Returns:
        str: the text in Turkish-aware lower case ("I" -> "ı", "İ" -> "i") with single spaces.
    """
    lowered = text.replace("I", "ı").replace("İ", "i").lower()
    return re.sub(r"\s+", " ", lowered)


def is_decline(text):
    """Tell whether a model reply is the fixed decline reply.

    A reply counts as a decline when it starts with DECLINE_REPLY, ignoring letter case,
    line breaks and wrapping characters such as quotes, asterisks or a missing final
    period. Anything the model wrote after the sentence does not change the result;
    answer.py replaces the whole reply with DECLINE_REPLY, so no half-answer is shown.

    Args:
        text (str | None): the reply of the answer model.

    Returns:
        bool: True if the reply is a decline, False otherwise (also for an empty reply).
    """
    if not text:
        return False
    reply = _normalize(text.lstrip(_WRAPPING))
    target = _normalize(DECLINE_REPLY).rstrip(".")
    return reply.startswith(target)


# --- CHUNKY-182: individual-case rule -------------------------------------------------
# When the user asks what to do in their own case (for example whether to contest a fine),
# the prompt (prompts/answer_v3.txt, rule 7) tells the model to state what the texts say,
# give no advice, and end the answer with exactly this sentence.
ADVICE_NOTICE = (
    "Asistan, kişisel durumunuz için tavsiye vermez; "
    "yukarıdakiler yalnızca mevzuat metinlerinin ne söylediğidir."
)

# Wordings that advise the user on a choice. Used only to flag answers for a human to read
# (notebooks/06_decline_check.ipynb); they are not removed from the answer.
_ADVICE_PHRASES = (
    "tavsiye ederim", "tavsiye ederiz", "tavsiyem", "öneririm", "öneririz", "önerim",
    "bence", "kanımca", "itiraz etmelisiniz", "itiraz etmenizi", "itiraz etmeniz iyi olur",
    "itiraz etmeyin", "ödemelisiniz", "ödemenizi öner", "dava açmalısınız", "başvurmalısınız",
    "beklemelisiniz", "kazanırsınız", "kazanma şansınız", "yapmanız en doğrusu", "en iyisi",
)


def has_advice_notice(text):
    """Tell whether an answer carries the fixed individual-case notice.

    Args:
        text (str | None): the answer of the model.

    Returns:
        bool: True if ADVICE_NOTICE appears in the answer (letter case, line breaks and
        the final period are ignored), False otherwise.
    """
    if not text:
        return False
    return _normalize(ADVICE_NOTICE).rstrip(".") in _normalize(text)


def find_advice_phrases(text):
    """List the advising wordings found in an answer, outside the fixed notice.

    Args:
        text (str | None): the answer of the model.

    Returns:
        list[str]: the phrases of _ADVICE_PHRASES that occur in the answer, in list order;
        empty if none. The fixed notice itself ("tavsiye vermez") is not counted.
    """
    if not text:
        return []
    body = _normalize(text).replace(_normalize(ADVICE_NOTICE).rstrip("."), " ")
    return [p for p in _ADVICE_PHRASES if _normalize(p) in body]

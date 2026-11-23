"""Decline path: the fixed reply for questions outside the six texts.

Added by barissaka for CHUNKY-130 (US-06 Decline when the assistant does not know),
sub-task CHUNKY-181.

The answer prompt (prompts/answer_v2.txt) tells the model to reply with exactly
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
# prompts/answer_v2.txt must contain it word for word (checked by tests/test_guard.py).
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

"""
Copyright 2025 RobotsMali AI4D Lab.

Licensed under the MIT License; you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

https://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
try:
    import regex  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback when regex isn't installed
    regex = None

from .basic_bam_normalizer import BasicBambaraNormalizer

# -----------------------------------------------------------------------------
# number conversion helpers
# -----------------------------------------------------------------------------

UNITS_BAM = [
    "fu",
    "kelen",
    "fila",
    "saba",
    "naani",
    "duuru",
    "wɔɔrɔ",
    "wolonwula",
    "seegin",
    "kɔnɔntɔn",
]


def number_to_bambara(n: int) -> str:
    """Recursive Bambara number to words (supports up to millions)."""
    units = UNITS_BAM
    tens = [
        "",
        "tan",
        "mugan",
        "bi saba",
        "bi naani",
        "bi duuru",
        "bi wɔɔrɔ",
        "bi wolonfila",
        "bi seegin",
        "bi kɔnɔntɔn",
    ]
    if n == 0:
        return "fu"
    if n < 10:
        return units[n]
    if n < 100:
        if n < 20:
            return tens[n // 10]
        return tens[n // 10] + (" ni " + number_to_bambara(n % 10) if n % 10 else "")
    if n < 1000:
        prefix = "kɛmɛ" if n < 200 else "kɛmɛ " + number_to_bambara(n // 100)
        return prefix + (" ni " + number_to_bambara(n % 100) if n % 100 else "")
    if n < 1_000_000:
        return "waa " + number_to_bambara(n // 1000) + (
            " ni " + number_to_bambara(n % 1000) if n % 1000 else ""
        )
    return "milyɔn " + number_to_bambara(n // 1_000_000) + (
        " ni " + number_to_bambara(n % 1_000_000) if n % 1_000_000 else ""
    )


def bambara_words_to_number(phrase: str) -> int:
    """Convert a Bambara number phrase into an integer."""
    units = {
        "fu": 0,
        "kelen": 1,
        "fila": 2,
        "saba": 3,
        "naani": 4,
        "duuru": 5,
        "wɔɔrɔ": 6,
        "wolonwula": 7,
        "seegin": 8,
        "kɔnɔntɔn": 9,
    }
    tens = {
        "tan": 10,
        "mugan": 20,
        "bi saba": 30,
        "bi naani": 40,
        "bi duuru": 50,
        "bi wɔɔrɔ": 60,
        "bi wolonfila": 70,
        "bi seegin": 80,
        "bi kɔnɔntɔn": 90,
    }

    # Single token values
    token_map = {**units, **tens, "kɛmɛ": 100}

    parts = [p.strip() for p in phrase.strip().split("ni") if p.strip()]
    total = 0

    for part in parts:
        tokens = part.split()
        if not tokens:
            continue

        if tokens[0] == "waa":  # e.g. "waa duuru"
            multiplier = bambara_words_to_number(" ".join(tokens[1:])) if len(tokens) > 1 else 1
            total += 1000 * multiplier

        elif tokens[0] == "milyɔn":
            multiplier = bambara_words_to_number(" ".join(tokens[1:])) if len(tokens) > 1 else 1
            total += 1_000_000 * multiplier

        elif tokens[0] == "kɛmɛ":
            multiplier = bambara_words_to_number(" ".join(tokens[1:])) if len(tokens) > 1 else 1
            total += 100 * multiplier

        else:
            token = " ".join(tokens)
            if token in token_map:
                total += token_map[token]
            else:
                raise ValueError(f"Unrecognized token: {token}. Check for a syntax error")

    return total


# tokens that may appear in number phrases
NUMBER_WORD_TOKENS = {
    "fu",
    "kelen",
    "fila",
    "saba",
    "naani",
    "duuru",
    "wɔɔrɔ",
    "wolonwula",
    "seegin",
    "kɔnɔntɔn",
    "tan",
    "mugan",
    "bi",
    "wolonfila",
    "kɛmɛ",
    "waa",
    "milyɔn",
    "tomi",
    "ni",
}


class BambaraNumberNormalizer(BasicBambaraNormalizer):
    """Normalize and denormalize numbers within Bambara text. Support up to millions"""

    def _normalize_number_token(self, token: str) -> str:
        if token.count(".") == 1:
            left, right = token.split(".")
            if len(right) == 1:
                return (
                    f"{number_to_bambara(int(left))} tomi {number_to_bambara(int(right))}"
                )

        if "." in token:
            parts = token.split(".")
            if all(len(p) == 3 for p in parts[1:]):
                token = "".join(parts)
            else:
                token = parts[0] + "".join(parts[1:])

        if token.startswith("0") and len(token) > 1:
            digits = [int(d) for d in token]
            return " ni ".join(UNITS_BAM[d] for d in digits)

        n = int(token)
        return number_to_bambara(n)

    def __call__(self, s: str):
        s = s.lower()
        s = re.sub(r"[<\[][^>\]]*[>\]]", "", s)
        s = re.sub(r"\(([^)]+?)\)", "", s)
        s = re.sub(r"\d[\d\.]*", lambda m: self._normalize_number_token(m.group(0)), s)
        s = self.clean(s).lower()

        if self.split_letters:
            if regex:
                s = " ".join(regex.findall(r"\X", s, re.U))
            else:
                s = " ".join(list(s))

        s = re.sub(r"\s+", " ", s)
        return s.strip()

    def _denormalize_buffer(self, tokens):
        phrase = " ".join(tokens)
        if "tomi" in tokens:
            idx = tokens.index("tomi")
            left_phrase = " ".join(tokens[:idx])
            right_phrase = " ".join(tokens[idx + 1 :])
            try:
                left = bambara_words_to_number(left_phrase) if left_phrase else 0
                right = bambara_words_to_number(right_phrase) if right_phrase else 0
                return f"{left}.{right}"
            except ValueError:
                return phrase
        try:
            return str(bambara_words_to_number(phrase))
        except ValueError:
            return phrase

    def denormalize(self, s: str) -> str:
        """Denormalize a Bambara number phrase and return its numeral form.

        Args:
            s (str): The spelled out number in proper Bambara syntax

        Returns:
            str: The numeral form of the number phrase.
        """
        tokens = s.lower().split()
        result = []
        buf = []
        for t in tokens:
            if t in NUMBER_WORD_TOKENS:
                buf.append(t)
            else:
                if buf:
                    result.append(self._denormalize_buffer(buf))
                    buf = []
                result.append(t)
        if buf:
            result.append(self._denormalize_buffer(buf))
        return " ".join(result)


__all__ = ["BambaraNumberNormalizer"]

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


def number_to_bambara(n: int, is_money: bool = False) -> str:
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
        "bi wolonwula",
        "bi seegin",
        "bi kɔnɔntɔn",
    ]
    
    if is_money:
        if n < 1_000_000:
            n //= 5  # Convert from CFA counting to actual number
            
        if n == 0:
            return "fu"
        if n < 10:
            return "dɔrɔmɛ " + units[n]
        if n < 100:
            # INSIDE magnitude (Tens & Units): use "ni"
            return tens[n // 10] + (" ni " + number_to_bambara(n % 10) if n % 10 else "")
        if n < 1000:
            # CROSSING magnitude (Hundreds to remainder): use "ani"
            prefix = "kɛmɛ" if n < 200 else "kɛmɛ " + number_to_bambara(n // 100)
            return prefix + (" ni " + number_to_bambara(n % 100) if n % 100 else "")
        if n < 1_000_000:
            return "waa " + number_to_bambara(n // 1000) + (
                " ani " + number_to_bambara(n % 1000) if n % 1000 else ""
            )
        return "milyɔn " + number_to_bambara(n // 1_000_000) + (
            " ani " + number_to_bambara(n % 1_000_000, is_money=True) if n % 1_000_000 else ""
        )
    else:
        if n == 0:
            return "fu"
        if n < 10:
            return units[n]
        if n < 100:
            return tens[n // 10] + (" ni " + number_to_bambara(n % 10) if n % 10 else "")
        if n < 1000:
            prefix = "kɛmɛ" if n < 200 else "kɛmɛ " + number_to_bambara(n // 100)
            return prefix + (" ni " + number_to_bambara(n % 100) if n % 100 else "")
        if n < 1_000_000:
            return "waa " + number_to_bambara(n // 1000) + (
                " ani " + number_to_bambara(n % 1000) if n % 1000 else ""
            )
        return "milyɔn " + number_to_bambara(n // 1_000_000) + (
            " ani " + number_to_bambara(n % 1_000_000) if n % 1_000_000 else ""
        )

def bambara_words_to_number(phrase: str, is_money: bool = False) -> int:
    """Convert a Bambara number phrase into an integer."""
    # Clean up the money prefix immediately as it has no numeric counting value 
    # (The CFA scaling is handled at the end)
    phrase = phrase.replace("dɔrɔmɛ ", "").strip()
    
    if not phrase or phrase == "fu":
        return 0

    # We both 'wolonwula' and 'wolonfila' to make it robust to dialect variations
    units = {
        "kelen": 1, "fila": 2, "saba": 3, "naani": 4, "duuru": 5,
        "wɔɔrɔ": 6, "wolonwula": 7, "wolonfila": 7, "seegin": 8, "kɔnɔntɔn": 9,
    }
    tens = {
        "tan": 10, "mugan": 20, "bi saba": 30, "bi naani": 40,
        "bi duuru": 50, "bi wɔɔrɔ": 60, "bi wolonwula": 70, "bi wolonfila": 70,
        "bi seegin": 80, "bi kɔnɔntɔn": 90,
    }
    
    token_map = {**units, **tens}

    def parse_block(block: str) -> int:
        """Recursively evaluate a chunk of text without 'ani' separators."""
        block = block.strip()
        if not block:
            return 0

        # 1. Evaluate Millions multiplier
        if block.startswith("milyɔn"):
            remainder = block.replace("milyɔn", "", 1).strip()
            multiplier = parse_block(remainder) if remainder else 1
            return 1_000_000 * multiplier

        # 2. Evaluate Thousands multiplier
        if block.startswith("waa"):
            remainder = block.replace("waa", "", 1).strip()
            multiplier = parse_block(remainder) if remainder else 1
            return 1000 * multiplier

        # 3. Evaluate Hundreds, Tens, Units
        parts = [p.strip() for p in block.split(" ni ") if p.strip()]
        block_total = 0
        
        for part in parts:
            if not part:
                continue
            if part.startswith("kɛmɛ"):
                # E.g., "kɛmɛ naani" -> extract "naani", calculate 100 * 4
                mult_str = part.replace("kɛmɛ", "", 1).strip()
                mult = token_map.get(mult_str, 1) if mult_str else 1
                block_total += 100 * mult
            elif part in token_map:
                block_total += token_map[part]
            else:
                raise ValueError(f"Unrecognized token: '{part}'. Check for a syntax error.")
                
        return block_total

    major_blocks = phrase.split(" ani ")
    
    # We just parse each block and sum them all together
    total = sum(parse_block(block) for block in major_blocks)

    if is_money:
        if total >= 1_000_000:
            total = (total // 1_000_000) * 1_000_000 + (total % 1_000_000) * 5
        else:
            total = total * 5

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
    "ni",
    "ani"}


class BambaraNumberNormalizer(BasicBambaraNormalizer):
    """Normalize and denormalize numbers within Bambara text. Support up to millions"""

    def _normalize_number_token(self, token: str, is_money: bool = False) -> str:
        if "." in token:
            parts = token.split(".")
            token = "".join(parts)

        if token.startswith("0") and len(token) > 1:
            digits = [int(d) for d in token]
            return " ni ".join(UNITS_BAM[d] for d in digits)

        n = int(token)
        return number_to_bambara(n, is_money=is_money)

    def __call__(self, s: str, is_money: bool = False) -> str:
        s = s.lower()
        s = re.sub(r"[<\[][^>\]]*[>\]]", "", s)
        s = re.sub(r"\(([^)]+?)\)", "", s)
        s = re.sub(r"\d[\d\.]*", lambda m: self._normalize_number_token(m.group(0), is_money=is_money), s)

        if self.split_letters:
            if regex:
                s = " ".join(regex.findall(r"\X", s, re.U))
            else:
                s = " ".join(list(s))

        s = re.sub(r"\s+", " ", s)
        return s.strip()

    def _denormalize_buffer(self, tokens, is_money: bool = False) -> str:
        phrase = " ".join(tokens)
        try:
            return str(bambara_words_to_number(phrase, is_money=is_money))
        except ValueError:
            return phrase

    def denormalize(self, s: str, is_money: bool = False) -> str:
        """Denormalize a Bambara number phrase and return its numeral form.

        Args:
            s (str): The spelled out number in proper Bambara syntax
            is_money (bool): Whether the number represents a money amount

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
                    result.append(self._denormalize_buffer(buf, is_money=is_money))
                    buf = []
                result.append(t)
        if buf:
            result.append(self._denormalize_buffer(buf, is_money=is_money))
        return " ".join(result)


__all__ = ["BambaraNumberNormalizer"]

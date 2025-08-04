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

import unicodedata
from .basic_text_normalizer import BasicTextNormalizer

# non-ASCII letters that are not separated by "NFKD" normalization
ADDITIONAL_DIACRITICS = {
    "œ": "oe",
    "Œ": "OE",
    "ø": "o",
    "Ø": "O",
    "æ": "ae",
    "Æ": "AE",
    "ß": "ss",
    "ẞ": "SS",
    "đ": "d",
    "Đ": "D",
    "ð": "d",
    "Ð": "D",
    "þ": "th",
    "Þ": "th",
    "ł": "l",
    "Ł": "L",
}

class BasicBambaraNormalizer(BasicTextNormalizer):
    """
    A normalizer for Bambara text that extends the BasicTextNormalizer.

    This normalizer can remove diacritics and split letters based on the provided options.
    """

    def __init__(self, remove_diacritics=True, split_letters=False):
        """
        Initialize the BasicBambaraNormalizer.

        Args:
            remove_diacritics (bool): Whether to remove diacritics. Defaults to True.
            split_letters (bool): Whether to split letters. Defaults to False.
        """
        # Remove diacritics by default since Bambara does not use them anymore
        # Only exception is the apostrophe, which is very common in new bambara lexicon
        super().__init__(remove_diacritics, split_letters)

    def remove_symbols(self, s: str, keep="'’"):
        """
        Replace any markers, symbols, and punctuations with a space, keeping specified characters.

        Hyphens between alphabetic characters are preserved to accommodate compound words influenced by French.

        Args:
            s (str): The input string.
            keep (str, optional): Characters to keep in the string. Defaults to "'".

        Returns:
            str: The string with symbols replaced by spaces.
        """
        normalized = unicodedata.normalize("NFKC", s)
        return "".join(
            (
                c
                if c in keep
                else (
                    c  # Keep hyphens only when between alphabetic characters (compound words)
                    if c == "-" and
                    0 < i < len(normalized) - 1 and
                    normalized[i - 1].isalpha() and
                    normalized[i + 1].isalpha()
                    else (
                        " " if unicodedata.category(c)[0] in "MSP" else c
                    )
                )
            )
            for i, c in enumerate(normalized)
        )

    def remove_symbols_and_diacritics(self, s: str, keep="'’"):
        """
        Replace any markers, symbols, and punctuations with a space, and remove any diacritics.

        Hyphens between alphabetic characters are preserved to accommodate compound words influenced by French.

        Args:
            s (str): The input string.
            keep (str, optional): Characters to keep in the string. Defaults to "'".

        Returns:
            str: The string with symbols replaced by spaces and diacritics removed.
        """
        normalized = unicodedata.normalize("NFKD", s)
        return "".join(
            (
                c
                if c in keep
                else (
                    ADDITIONAL_DIACRITICS[c]
                    if c in ADDITIONAL_DIACRITICS
                    else (
                        c  # Keep hyphens only when between alphabetic characters (compound words)
                        if c == "-" and
                        0 < i < len(normalized) - 1 and
                        normalized[i - 1].isalpha() and
                        normalized[i + 1].isalpha()
                        else (
                            ""
                            if unicodedata.category(c) == "Mn"
                            else " " if unicodedata.category(c)[0] in "MSP" else c
                        )
                    )
                )
            )
            for i, c in enumerate(normalized)
        )

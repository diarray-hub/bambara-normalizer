"""
Copyright (c) 2022 OpenAI

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
import unicodedata
try:
    import regex  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback when regex isn't installed
    regex = None

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

class BasicTextNormalizer:
    """
    A class used to normalize text by removing symbols, diacritics, and optionally splitting letters.
    """

    def __init__(self, remove_diacritics: bool = False, split_letters: bool = False):
        """
        Initialize the BasicTextNormalizer.

        Args:
            remove_diacritics (bool, optional): If True, diacritics will be removed from the text. Defaults to False.
            split_letters (bool, optional): If True, letters will be split into individual characters. Defaults to False.
        """
        self.clean = (
            self.remove_symbols_and_diacritics if remove_diacritics else self.remove_symbols
        )
        self.split_letters = split_letters

    def __call__(self, s: str):
        """
        Normalize the input string.

        Args:
            s (str): The input string to be normalized.

        Returns:
            str: The normalized string.
        """
        s = s.lower()
        s = re.sub(r"[<\[][^>\]]*[>\]]", "", s)  # remove words between brackets
        s = re.sub(r"\(([^)]+?)\)", "", s)  # remove words between parenthesis
        s = self.clean(s).lower()

        if self.split_letters:
            if regex:
                s = " ".join(regex.findall(r"\X", s, re.U))
            else:
                s = " ".join(list(s))

        s = re.sub(
            r"\s+", " ", s
        )  # replace any successive whitespace characters with a space

        return s.strip()

    def remove_symbols(self, s: str, keep=""):
        """
        Replace any markers, symbols, and punctuations with a space, keeping diacritics.

        Args:
            s (str): The input string.
            keep (str, optional): Characters to keep in the string. Defaults to "".

        Returns:
            str: The string with symbols replaced by spaces.
        """
        return "".join(
            (
                c
                if c in keep
                else (
                    " " if unicodedata.category(c)[0] in "MSP" else c
                )
            ) for c in unicodedata.normalize("NFKC", s)
        )

    def remove_symbols_and_diacritics(self, s: str, keep=""):
        """
            Replace any markers, symbols, and punctuations with a space, and drop any diacritics.

            Args:
                s (str): The input string.
                keep (str, optional): Characters to keep in the string. Defaults to "".

            Returns:
                str: The string with symbols replaced by spaces and diacritics removed.
            """
        return "".join(
            (
                c
                if c in keep
                else (
                    ADDITIONAL_DIACRITICS[c]
                    if c in ADDITIONAL_DIACRITICS
                    else (
                        ""
                        if unicodedata.category(c) == "Mn"
                        else " " if unicodedata.category(c)[0] in "MSP" else c
                    )
                )
            )
            for c in unicodedata.normalize("NFKD", s)
        )

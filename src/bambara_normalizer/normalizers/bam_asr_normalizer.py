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

class BambaraASRNormalizer(BasicBambaraNormalizer):
    """
    A normalizer for Bambara ASR text that extends the BasicBambaraNormalizer.
    """
    def __call__(self, s):
        """
        Normalize the input string.

        Args:
            s (str): The input string to be normalized.

        Returns:
            str: The normalized string.
        """
        # In ASR, standards for audio transcription can varie
        # but most of the time text in parenthesis or brackets is actually spoken in the audio
        # So removing them is not optimal
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

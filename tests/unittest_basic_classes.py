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
import unittest
from bambara_normalizer.normalizers import (
    BasicTextNormalizer,
    BasicBambaraNormalizer,
    BambaraASRNormalizer,
    BambaraNumberNormalizer,
)

class TestTextNormalizers(unittest.TestCase):

    def test_basic_text_normalizer(self):
        normalizer = BasicTextNormalizer(remove_diacritics=False, split_letters=False)
        self.assertEqual(normalizer("Hello, World!"), "hello world")
        self.assertEqual(normalizer("Test (remove) this."), "test this")
        self.assertEqual(normalizer("Symbols like @#$%^&*()"), "symbols like")

    def test_basic_text_normalizer_with_diacritics(self):
        normalizer = BasicTextNormalizer(remove_diacritics=True, split_letters=False)
        self.assertEqual(normalizer("cliché"), "cliche")
        self.assertEqual(normalizer("naïve"), "naive")

    def test_basic_text_normalizer_with_split_letters(self):
        normalizer = BasicTextNormalizer(remove_diacritics=False, split_letters=True)
        self.assertEqual(normalizer("abc"), "a b c")
        self.assertEqual(normalizer("Test123"), "t e s t 1 2 3")

    def test_basic_bambara_normalizer(self):
        normalizer = BasicBambaraNormalizer()
        self.assertEqual(normalizer("Bàmùn"), "bamun")
        self.assertEqual(normalizer("Compound-word"), "compound-word")
        self.assertEqual(normalizer("Text with (parenthesis) and [brackets]"), "text with and")

    def test_bambara_normalizer_with_split_letters(self):
        normalizer = BasicBambaraNormalizer(split_letters=True)
        self.assertEqual(normalizer("bambara"), "b a m b a r a")

    def test_bambara_asr_normalizer(self):
        normalizer = BambaraASRNormalizer()
        self.assertEqual(normalizer("Bàmùn"), "bamun")
        self.assertEqual(normalizer("- ni i ma dɔnkili da, (ni i ma dɔnkili laminɛ], an bɛɛ bɛ kɛ su ye sisan."),
                         "ni i ma dɔnkili da ni i ma dɔnkili laminɛ an bɛɛ bɛ kɛ su ye sisan")
        self.assertEqual(normalizer("Compound-word"), "compound-word")
        self.assertEqual(normalizer("Text with (parenthesis) and [brackets]"), "text with parenthesis and brackets")

    def test_bambara_asr_normalizer_with_split_letters(self):
        normalizer = BambaraASRNormalizer(split_letters=True)
        self.assertEqual(normalizer("asr test"), "a s r t e s t")

    def test_bambara_asr_readme_examples(self):
        normalizer = BambaraASRNormalizer()
        self.assertEqual(normalizer("sìrajɛ, - í ni tìle !"), "sirajɛ i ni tile")
        self.assertEqual(normalizer("(à kán) [kɛ̀nɛ]."), "a kan kɛnɛ")
        normalizer_split = BambaraASRNormalizer(split_letters=True)
        self.assertEqual(normalizer_split("ǹsé, í ni tìle !"), "n s e i n i t i l e")

    def test_bambara_number_normalizer(self):
        normalizer = BambaraNumberNormalizer()
        self.assertEqual(
            normalizer("N ye 35.4 tugu."),
            "n ye bi saba ni duuru tomi naani tugu",
        )
        self.assertEqual(
            normalizer("N na 35.000.000 frank."),
            "n na milyɔn bi saba ni duuru frank",
        )
        self.assertEqual(normalizer("kodoo 012."), "kodoo fu ni kɛlɛn ni fila")
        self.assertEqual(
            normalizer.denormalize("bi saba ni duuru tomi naani"), "35.4"
        )
        self.assertEqual(
            normalizer.denormalize("milyɔn bi saba ni duuru"), "35000000"
        )

if __name__ == "__main__":
    unittest.main()

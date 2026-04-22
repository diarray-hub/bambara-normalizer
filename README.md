# bambara-normalizer

`bambara-normalizer` is a Python package for normalizing Bambara text, tailored for Natural Language Processing (NLP) tasks. The package provides tools to preprocess text by removing symbols, diacritics, and performing additional transformations required for various NLP applications such as ***number normalization***.

## Features

- **BasicTextNormalizer**: A generic text normalization class that removes symbols, diacritics, and optionally splits letters.
- **BasicBambaraNormalizer**: Extends `BasicTextNormalizer` with specific rules for Bambara text, such as preserving hyphens in compound words and handling apostrophes.
- **BambaraASRNormalizer**: A specialized normalizer for Automatic Speech Recognition (ASR) tasks in Bambara, designed to retain parenthetical and bracketed text that might appear in spoken transcriptions.
- **BambaraNumberNormalizer**: Add number normalization capability to the package, both number2bam and bam2number including money amounts (Bambara 'dɔrɔmɛ' counting system where 5 CFA equals 1 dɔrɔmɛ) (up to millions)

## Installation

### Install from PyPI

To install the package, run:

```bash
pip install bambara-normalizer
```

### Install from Source

To install the package from source, clone the repository and build the package:

```bash
git clone https://github.com/diarray-hub/bambara-normalizer.git
cd bambara-normalizer
python -m build --wheel
pip install dist/bambara_normalizer-1.1.0-py3-none-any.whl
```

## Usage

### BasicTextNormalizer

```python
from bambara_normalizer import BasicTextNormalizer

normalizer = BasicTextNormalizer(remove_diacritics=True, split_letters=False)
text = "Cliché text with symbols & diacritics!"
normalized_text = normalizer(text)
print(normalized_text)  # Output: "cliche text with symbols diacritics"
```

### BasicBambaraNormalizer

```python
from bambara_normalizer import BasicBambaraNormalizer

normalizer = BasicBambaraNormalizer()
text = "à tɔ́gɔ kó : sìrajɛ."
normalized_text = normalizer(text)
print(normalized_text)  # Output: "a tɔgɔ ko sirajɛ"

# Example with hyphens
text_with_hyphens = "- bɛ̀n-kɛ́nɛfisɛ."
normalized_text = normalizer(text_with_hyphens)
print(normalized_text)  # Output: "bɛn-kɛnɛfisɛ"
```

### BambaraASRNormalizer

```python
from bambara_normalizer import BambaraASRNormalizer

normalizer = BambaraASRNormalizer()
text = "sìrajɛ, - í ni tìle !"
normalized_text = normalizer(text)
print(normalized_text)  # Output: "sirajɛ i ni tile"

# Example with words in parenthesis and brackets
text_with_brackets = "(à ká) [kɛ̀nɛ]."
normalized_text = normalizer(text_with_brackets)
print(normalized_text)  # Output: "a ka kɛnɛ"
```

### BambaraASRNormalizer with Split Letters

```python
from bambara_normalizer import BambaraASRNormalizer

normalizer = BambaraASRNormalizer(split_letters=True)
text = "ǹsé, í ni tìle !"
normalized_text = normalizer(text)
print(normalized_text)  # Output: "n s e i n i t i l e"
```

### Words to number

```python
>>> from bambara_normalizer import BambaraNumberNormalizer
>>> normalizer = BambaraNumberNormalizer()
>>> normalizer.denormalize("waa kɛmɛ ni bi duuru ni seegin")
'158000'
>>> normalizer.denormalize("waa bi saba ni kelen ani kɛmɛ wɔɔrɔ", is_money=True)
'158000'
```

### Number to Bambara
```python
>>> from bambara_normalizer import BambaraNumberNormalizer
>>> normalizer = BambaraNumberNormalizer()
>>> normalizer("158000")
'waa kɛmɛ ni bi duuru ni seegin'
>>> normalizer("158000", is_money=True)
'waa bi saba ni kelen ani kɛmɛ wɔɔrɔ'
# the token "ani" is used as a magnitude separator that separates the high magnitude units (milyɔn|waa|kɛmɛ)
# the token "ni" is used for summing into internal magnitude units
# Note that the denormalize function expects those tokens to hold those specific meanings
>>> num_norm("147.874.120", is_money=True)
'milyɔn kɛmɛ ni bi naani ni wolonwula ani waa kɛmɛ ni bi wolonwula ni naani ani kɛmɛ seegin ni mugan ni naani'
```

### BambaraNumberNormalizer (used on full sentences)

```python
from bambara_normalizer import BambaraNumberNormalizer

normalizer = BambaraNumberNormalizer()
text = "N ye 35000 tugu."
normalized_text = normalizer(text, is_money=True)
print(normalized_text)  # Output: "n ye waa wolunwula tugu"

# Large numbers and leading zeros
text2 = "N bɛ na 35.000.000 labɔ. Kɔdi ye 012."
normalized_text2 = normalizer(text2)
print(normalized_text2)  # Output: "n bɛ na milyɔn bi saba ni duuru labɔ. kɔdi ye fu ni kelen ni fila"

# Denormalization
print(normalizer.denormalize("milyɔn bi saba ni duuru"))  # Output: "35000000"
```

## Customization

Each normalizer supports optional parameters to better customize their behaviors:

- **Removing/Keeping diacritics**: Converts characters like `é` to `e`.
- **Splitting letters**: Converts `abc` to `a b c`.
- **Preserving specific symbols**: Customize which characters to retain (e.g., hyphens or apostrophes) with the 'keep' parameter of the base functions remove_symbols_and_diacritics and remove_symbols.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors

- [Yacouba Diarra @ RobotsMali AI4D Lab](https://github.com/diarray-hub)

***⚠️ Warning***: This package is not actively maintained

---

Feel free to reach out for any questions or support regarding the usage of this package!


# Bambara Normalizer v1.0.0

First update of the package. August 04, 2025

## Features

- **BambaraNumberNormalizer**: Add number normalization capability to the package, both number2bam and bam2number (up to millions)
- **Add wrap import**: You can now do `from bambara_normalizer import *` and import all the main classes

## Fixes

- **Preservation of curly apostrophes**: BasicBambaraNormalizer now keeps curly apostrophes too 
- **Better handling of second category dependencies**: The package doesn't functionnally depend on `regex` in this new version
- **Fixed typos and better documentation**

# Bambara Normalizer v0.0.1

First pre-release. January 17, 2025

## Features

- **BasicTextNormalizer**: A generic text normalization class that removes symbols, diacritics, and optionally splits letters.
- **BasicBambaraNormalizer**: Extends `BasicTextNormalizer` with specific rules for Bambara text, such as preserving hyphens in compound words and handling apostrophes.
- **BambaraASRNormalizer**: A specialized normalizer for Automatic Speech Recognition (ASR) tasks in Bambara, designed to retain parenthetical and bracketed text that might appear in spoken transcriptions.

## Install from PyPI

To install the package, run:

```bash
pip install bambara-normalizer==0.0.1
```
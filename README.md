# Quote Search Engine

A CLI-based search engine for [Quotes to Scrape](https://quotes.toscrape.com/).

## Features
- Full-site crawling with configurable delay.
- Inverted index construction with term frequency and position info.
- Intersection-based multi-word search.
- Interactive CLI interface.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the main script:
```bash
python src/main.py
```

### Commands
- `build`: Crawl the website and build the index.
- `load`: Load an existing index from the `data/` directory.
- `print <word>`: Display the inverted index entry for a specific word.
- `find <word1> [word2...]`: Search for quotes containing all specified words.
- `exit`: Quit the application.

## Project Structure
- `src/`: Core source code (crawler, indexer, search, main).
- `tests/`: Unit tests with mock networking.
- `data/`: Serialized index and document storage.

## GenAI Usage Declaration
- **AI Tool Used**: Windsurf (Cascade)
- **Purpose**: Full-cycle development including environment setup, core logic implementation, testing, and Git version control.
- **Quality Analysis**: The generated code follows PEP8, includes type hints, and implements defensive error handling. Tests provide >85% coverage for core modules.
- **Learning Impact**: Demonstrated efficient integration of web scraping, indexing algorithms, and CLI design using an automated agentic workflow.

import sys
from crawler import QuoteCrawler
from indexer import QuoteIndexer
from search import QuoteSearcher
import logging

def main():
    """
    Main CLI interactive loop.
    """
    indexer = QuoteIndexer()
    searcher = None

    print("Welcome to Quote Search Engine CLI")
    print("Available commands: build, load, print <word>, find <word1> [word2...], exit")

    while True:
        try:
            user_input = input("\n> ").strip().split()
            if not user_input:
                continue
            
            command = user_input[0].lower()
            args = user_input[1:]

            if command == "exit":
                break
            
            elif command == "build":
                print("Building index... (this may take a while)")
                crawler = QuoteCrawler()
                quotes = crawler.crawl_all_quotes()
                indexer.build_index(quotes)
                indexer.save_index()
                searcher = QuoteSearcher(indexer.index, indexer.documents)
                print(f"Successfully built and saved index with {len(quotes)} quotes.")

            elif command == "load":
                try:
                    indexer.load_index()
                    searcher = QuoteSearcher(indexer.index, indexer.documents)
                    print(f"Successfully loaded index with {len(indexer.documents)} quotes.")
                except FileNotFoundError as e:
                    print(f"Error: {e}")

            elif command == "print":
                if not args:
                    print("Usage: print <word>")
                    continue
                
                if not searcher:
                    print("Error: Index not loaded. Run 'load' or 'build' first.")
                    continue
                
                word = args[0]
                info = indexer.get_word_index(word)
                if not info:
                    print(f"Word '{word}' not found in index.")
                else:
                    print(f"Index for '{word}':")
                    print(f"  Total Frequency: {info['total_frequency']}")
                    print(f"  Document Count: {info['document_count']}")
                    print(f"  Occurrences (DocID: Positions): {info['occurrences']}")

            elif command == "find":
                if not args:
                    print("Usage: find <word1> [word2...]")
                    continue
                
                if not searcher:
                    print("Error: Index not loaded. Run 'load' or 'build' first.")
                    continue
                
                results = searcher.find(args)
                if not results:
                    print("No matching quotes found.")
                else:
                    print(f"Found {len(results)} matching quotes:")
                    for i, res in enumerate(results, 1):
                        print(f"\n[{i}] \"{res['text']}\"")
                        print(f"    -- {res['author']}")
                        print(f"    Tags: {res['tags']}")
                        print(f"    URL: {res['url']}")

            else:
                print(f"Unknown command: {command}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

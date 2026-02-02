#!/usr/bin/env python3
"""ETL Pipeline: Parse XML to JSON"""

import sys
import os

# Get parent directory (repo root)
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(repo_root, 'dsa'))
os.chdir(repo_root)

from parse_xml import parse_xml, save_to_json

XML_FILE = "raw/momo.xml"
JSON_OUTPUT = "data/transactions.json"

def main():
    print("ETL Pipeline Starting...\n")
    
    # Parse XML
    print(f"1. Parsing: {XML_FILE}")
    transactions = parse_xml(XML_FILE)
    print(f"   ✓ {len(transactions)} transactions parsed\n")
    
    # Save JSON
    print(f"2. Saving: {JSON_OUTPUT}")
    save_to_json(transactions, JSON_OUTPUT)
    
    print("\n✓ Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
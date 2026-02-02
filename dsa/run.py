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
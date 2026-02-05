import time
import random
import os
import sys

# Add the current directory to Python path so we can import modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from xml_parser import parse_xml


# Search Algorithms

def linear_search(transactions, target_id):
    """
    Linear search through a list of transactions.
    Time Complexity: O(n)
    """
    for trans in transactions:
        if trans["id"] == target_id:
            return trans
    return None


def build_transaction_dict(transactions):
    """
    Build a dictionary mapping id -> transaction.
    Time Complexity: O(n)
    """
    return {trans["id"]: trans for trans in transactions}


def dict_lookup(trans_dict, target_id):
    """
    Dictionary lookup using transaction ID as key.
    Time Complexity: O(1) average case
    """
    return trans_dict.get(target_id)


# Performance Testing

def compare_search_performance(transactions, runs=5):
    """
    Compare linear search vs dictionary lookup.
    """
    # Make sure we have at least 20 records to test with
    if len(transactions) < 20:
        transactions = transactions * (20 // len(transactions) + 1)

    # Select a random transaction ID to search for
    target_id = random.choice(transactions)["id"]

    # Measure linear search performance
    linear_times = []
    for _ in range(runs):
        start = time.perf_counter()
        linear_search(transactions, target_id)
        linear_times.append(time.perf_counter() - start)

    avg_linear_time = sum(linear_times) / runs

    # Measure dictionary lookup performance
    trans_dict = build_transaction_dict(transactions)

    dict_times = []
    for _ in range(runs):
        start = time.perf_counter()
        dict_lookup(trans_dict, target_id)
        dict_times.append(time.perf_counter() - start)

    avg_dict_time = sum(dict_times) / runs

    return avg_linear_time, avg_dict_time


# Run performance comparison when this file is executed directly

if __name__ == "__main__":
    xml_path = os.path.join(BASE_DIR, "modified_sms_V2.xml")
    transactions = parse_xml(xml_path)

    linear_time, dict_time = compare_search_performance(transactions)

    print("DSA SEARCH PERFORMANCE COMPARISON\n")
    print(f"Number of transactions tested: {len(transactions)}")
    print(f"Average Linear Search Time: {linear_time:.8f} seconds")
    print(f"Average Dictionary Lookup Time: {dict_time:.8f} seconds")

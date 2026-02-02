"""
XML Parser: Convert SMS records from XML to JSON
"""
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime


def parse_xml(xml_file):
    """Parse XML and return list of transaction dictionaries"""
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    transactions = []
    tx_id = 1
    
    for sms in root.findall('sms'):
        body = sms.get('body', '')
        
        # Skip OTP and empty messages
        if "one-time password" in body or not body.strip():
            continue
        
        sms_date = sms.get('date')
        address = sms.get('address', 'Unknown')
        
        # Process M-Money transactions only
        if address == 'M-Money':
            # Extract data from SMS
            amount = extract_amount(body)
            tx_type = get_transaction_type(body)
            sender = extract_sender(body, tx_type)
            receiver = extract_receiver(body, tx_type)
            timestamp = convert_timestamp(sms_date)
            
            if amount > 0:
                transaction = {
                    'id': tx_id,
                    'transaction_type': tx_type,
                    'amount': amount,
                    'sender': sender,
                    'receiver': receiver,
                    'timestamp': timestamp
                }
                transactions.append(transaction)
                tx_id += 1
    
    return transactions


def extract_amount(body):
    """Extract amount from SMS body"""
    matches = re.findall(r'(\d+(?:,\d+)*)\s*RWF', body)
    if matches:
        return int(matches[0].replace(',', ''))
    return 0


def get_transaction_type(body):
    """Determine transaction type from SMS content"""
    if "received" in body.lower():
        return "receive"
    elif "*165*S*" in body or "transferred" in body:
        return "transfer"
    elif "payment" in body.lower() or "TxId:" in body:
        return "payment"
    elif "*113*R*" in body or "deposit" in body.lower():
        return "deposit"
    elif "withdrawn" in body.lower():
        return "withdrawal"
    elif "*162*" in body or "Airtime" in body:
        return "airtime"
    else:
        return "unknown"


def extract_sender(body, tx_type):
    """Extract sender name"""
    if tx_type == "receive":
        match = re.search(r'from\s+([A-Za-z\s]+)\s*\(', body)
        return match.group(1).strip() if match else "Unknown"
    elif tx_type == "deposit":
        return "Bank"
    else:
        return "You"


def extract_receiver(body, tx_type):
    """Extract receiver name"""
    if tx_type == "receive":
        return "Account Holder"
    elif tx_type == "transfer":
        match = re.search(r'to\s+([A-Za-z\s]+)\s*\(', body)
        return match.group(1).strip() if match else "Unknown"
    elif tx_type == "payment":
        match = re.search(r'to\s+([A-Za-z\s0-9]+)', body)
        return match.group(1).strip() if match else "Unknown"
    elif tx_type == "deposit":
        return "You"
    else:
        return "Unknown"


def convert_timestamp(ms_timestamp):
    """Convert milliseconds to ISO format"""
    try:
        return datetime.fromtimestamp(int(ms_timestamp) / 1000).isoformat()
    except:
        return datetime.now().isoformat()


def save_to_json(transactions, output_file):
    """Save transactions to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved {len(transactions)} transactions to {output_file}")
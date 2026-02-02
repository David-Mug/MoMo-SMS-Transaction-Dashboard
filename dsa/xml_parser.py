import xml.etree.ElementTree as ET #import an inbuilt python library to parse the data
import re #import regex library to help us extract necessary attributes from the body of the sms

def parse_xml(file_path):

    tree = ET.parse("modified_sms_V2.xml")  #Load the xml file and buiild the tree structure
    root = tree.getroot()   #access the root element

    transactions = []   #create an empty list to store the transaction attributes we need.

    for identity, sms in enumerate(root.findall("sms"), start=1):   #loop over the "sms" element representing transactions
    
        #extract the necessary attributes
        body = sms.attrib.get("body","")
        readable_date = sms.attrib.get("readable_date")

        #extracting amount
        match_amount = re.search(r"(\d[\d,]*) RWF", body)
        amount = match_amount.group(1).replace(",", "") if match_amount else None

        #Determine and extract transaction type
        if "received" in body.lower():
            transaction_type = "received"
        elif "payment" in body.lower() or "transferred" in body.lower():
            transaction_type = "payment"
        elif "deposit" in body.lower():
            transaction_type = "deposit"
        else:
            transaction_type = "unknown"

        #Extract sender (if "from" exists)
        match_sender = re.search(r"from ([\w\s\*\(\)]+?) \(.*\)", body)
        sender = match_sender.group(1) if match_sender else None

        # Extract receiver (if "to" exists)
        match_receiver = re.search(r"to ([\w\s\*\d]+?)[\s\.,]", body)
        receiver = match_receiver.group(1) if match_receiver else None

        transaction = {
            "id": identity,
            "transaction_type": transaction_type,
            "amount": amount,
            "receiver": receiver,
            "sender": sender,
            "readable_date": readable_date
        }
        
        transactions.append(transaction)
    return transactions


# for i in range(10):
#     print(transactions[i])
# #print just to confirm we are accessing the data correctly.

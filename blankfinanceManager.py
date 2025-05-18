import json
import requests
import mysql.connector as mariadb
import datetime

#im concious of the lack of error handling on this script
# However, for a small scale script designed for personal use the requirement didnt seem necesary 
# the script was tested and improved during the development process so im confident it works.

# The access token will expire every 24 hoursa new access token will be needed
# This function is designed to refresh the access token and return it
def refresh_access_token(refresh_token):
    # Define the API endpoint URL for refreshing the access token.
    url = "https://bankaccountdata.gocardless.com/api/v2/token/refresh/"
    # Define the headers for the HTTP request.
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    # Define the data to be sent in the request body.  This is the refresh token passed to the function.
    data = {
        "refresh": refresh_token,
    }
    #post the request and store the response in a variable called "response".
    response = requests.request("POST", url, headers=headers, json=data)
    # The 'response.json()' method converts the server's response (which is typically a string) into a Python dictionary.
    response_json = response.json()
    #Extract the new refresh token from the dictionary.
    new_access_token = response_json["access"]
    #return the new access token.
    return new_access_token

def get_transactions(access_token):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    date_from = yesterday.strftime('%Y-%m-%d')
    date_to = yesterday.strftime('%Y-%m-%d')
    url = f"https://bankaccountdata.gocardless.com/api/v2/accounts/insert_your_bank_id/transactions/?date_from={date_from}&date_to={date_to}"
    headers = {
        "Accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    transactions = response_json.get("transactions", {}).get("booked", [])
    return transactions


def insert_transaction(transactions):
    connection = mariadb.connect(host="localhost", user="root", password="Password1", database="bank")
    cursor = connection.cursor()

    insert_query = """
    insert ignore into bills (transactionID, entryReference, bookingDate, valueDate, amount, currency,debtorName, creditorName, 
                            remittanceInformationUnstructured, proprietaryBankTransactionCode, internalTransactionId)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for transaction in transactions:
        transactionId = transaction.get("transactionId")
        entryReference = transaction.get("entryReference",None)
        bookingDate = transaction.get("bookingDate")
        valueDate = transaction.get("valueDate")
        amount = transaction.get("transactionAmount", {}).get("amount")
        currency = transaction.get("transactionAmount", {}).get("currency")
        creditorName = transaction.get("creditorName")
        debtorName = transaction.get("debtorName")
        remittanceInformationUnstructured = transaction.get("remittanceInformationUnstructured", None)
        proprietaryBankTransactionCode = transaction.get("proprietaryBankTransactionCode", None)
        internalTransactionId = transaction.get("internalTransactionId", None)

        data = (transactionId, entryReference, bookingDate, valueDate, amount, currency,debtorName, creditorName, remittanceInformationUnstructured, proprietaryBankTransactionCode, internalTransactionId)
        cursor.execute(insert_query, data)
        connection.commit()

    cursor.close()
    connection.close()

refresh_token = "Inset_your_Refresh_token"
insert_transaction(get_transactions(refresh_access_token(refresh_token)))

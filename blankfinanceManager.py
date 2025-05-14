import json
import requests
import mysql.connector as mariadb
import datetime

# The access token will expire every 24 hoursa new access token will be needed
def refresh_access_token(refresh_token):
    url = "https://bankaccountdata.gocardless.com/api/v2/token/refresh/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {
        "refresh": refresh_token,
    }
    response = requests.request("POST", url, headers=headers, json=data)
    response_json = response.json()
    new_access_token = response_json["access"]
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
new_access_token = refresh_access_token(refresh_token)
transactions = get_transactions(new_access_token)
insert_transaction(transactions)

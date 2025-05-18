# financeManager
The project:

The finance manager project is designed to autmatically pull transactional data from my bank account, and insert into a Database ready to be analysed
there are 3 compenants to the script, refreshing the access token, pulling the transactions, and inserting the transactions into the DB. This will be broken down
into 3 functions that will be called within the main function, it should avoid any hard coding for ease of use.

Goals

1.) Automatically refresh the access token (expires every 24hours)

2.) Automatically pull the previous days transactions from my bank account

3.) Automatically Insert the transactions into a Database

4.) Analyse the data using PowerBI or Grafana.

Technologies

1.) GoCardlessAPI

2.) Python

3.) Linux (ubuntu)

3.) MySql DB (MariaDB)


Setting up the GoCardLess API

You can either use CLI or postman
I used postman because the GUI is easier to use in my opinion

Step 1)

Create a personal account with https://gocardless.com/

Step 2)

Setup a new Secret here - https://bankaccountdata.gocardless.com/user-secrets/
this will be essential for your security ID and your security key which will be used for everything.

Step 3)

Get your access Token
curl -X POST "https://bankaccountdata.gocardless.com/api/v2/token/new/" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
            "secret_id": "$SECRET_ID",
            "secret_key": "$SECRET_KEY"
        }'

Step 4)

Get your Bank ID (referred to as institution id)
curl -X GET "https://bankaccountdata.gocardless.com/api/v2/institutions/?country=gb" \
  -H  "accept: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN"

Step 5)

Create End user agreement
replace your access token and institution

curl -X POST "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/" \
  -H  "accept: application/json" \
  -H  "Content-Type: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN" \
  -d "{\"institution_id\": \"REVOLUT_REVOGB21\",
       \"max_historical_days\": \"180\",
       \"access_valid_for_days\": \"30\",
       \"access_scope\": [\"balances\", \"details\", \"transactions\"] }"

Step 6)

Build a link

acess token (from step 3)
Institution id (from step 4)
Reference (is unique but can be anything)
agreement (from step 5)

curl -X POST "https://bankaccountdata.gocardless.com/api/v2/requisitions/" \
  -H  "accept: application/json" -H  "Content-Type: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN" \
  -d "{\"redirect\": \"http://www.yourwebpage.com\",
       \"institution_id\": \"REVOLUT_REVOGB21\",
       \"reference\": \"124151\",
       \"agreement\": \"2dea1b84-97b0-4cb4-8805-302c227587c8\",
       \"user_language\":\"EN\" }"

Step 7)

list your accounts
you need to pass the requisition id from step 6 into the URL
change your access token

curl -X GET "https://bankaccountdata.gocardless.com/api/v2/requisitions/8126e9fb-93c9-4228-937c-68f0383c2df7/" \
  -H  "accept: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN" 

Step 8)
Retrieve your transactions
Pass one of your account ids into the url

curl -X GET "https://bankaccountdata.gocardless.com/api/v2/accounts/065da497-e6af-4950-88ed-2edbc0577d20/transactions/" \
  -H  "accept: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN"


replace your access token and institution

curl -X POST "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/" \
  -H  "accept: application/json" \
  -H  "Content-Type: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN" \
  -d "{\"institution_id\": \"REVOLUT_REVOGB21\",
       \"max_historical_days\": \"180\",
       \"access_valid_for_days\": \"30\",
       \"access_scope\": [\"balances\", \"details\", \"transactions\"] }"

Step6

Build a link

acess token (from step 3)
Institution id (from step 4)
Reference (is unique but can be anything)
agreement (from step 5)

curl -X POST "https://bankaccountdata.gocardless.com/api/v2/requisitions/" \
  -H  "accept: application/json" -H  "Content-Type: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN" \
  -d "{\"redirect\": \"http://www.yourwebpage.com\",
       \"institution_id\": \"REVOLUT_REVOGB21\",
       \"reference\": \"124151\",
       \"agreement\": \"2dea1b84-97b0-4cb4-8805-302c227587c8\",
       \"user_language\":\"EN\" }"

Step7

list your accounts
you need to pass the requisition id from step 6 into the URL
change your access token

curl -X GET "https://bankaccountdata.gocardless.com/api/v2/requisitions/8126e9fb-93c9-4228-937c-68f0383c2df7/" \
  -H  "accept: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN" 

Step8

Retrieve your transactions
Pass one of your account ids into the url

curl -X GET "https://bankaccountdata.gocardless.com/api/v2/accounts/065da497-e6af-4950-88ed-2edbc0577d20/transactions/" \
  -H  "accept: application/json" \
  -H  "Authorization: Bearer ACCESS_TOKEN"




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

Now that you have authenticated the goCardLess api with your bank
you should have 2 very important keys
  1) access token
  2) refresh token
We can move onto the next step - creating the MariaDB structure
i have a Database called Bank and a table called Bills
probably not the best naming convention for a large scale application but effective for what i want
![image](https://github.com/user-attachments/assets/ca262f23-9b39-4d3c-86b7-8d4b3b5822f0)

The bills table is setup as below

![image](https://github.com/user-attachments/assets/f1ed1271-57ec-4241-8739-78707ac5b366)

i wanted to make sure each transaction inserted had a unique identifer.
easiest way was ensuring each column was linked to a primary key

![image](https://github.com/user-attachments/assets/882ffab6-851d-4718-a4f7-6c381b92af24)

using a simple select statement we can see an example of the data that we are going to be working with
its worth noting here that the "amount" is in a double format which is not effective for currency
this data was inserted before i fixed this blunder.

![image](https://github.com/user-attachments/assets/c102e7f3-6086-4c77-8bf7-80f469ac22c3)


Here we have the cronjob we setup to automatically run the python script
this is currently ran on an ubuntu VM - but this will be moved to a Raspbery pi 4b
this is so the script can be ran everyday without my laptop being left on - Raspberry pi is much small form factor and significantly less power draw.

![image](https://github.com/user-attachments/assets/1cf17fc6-389c-438d-ac51-9756078fd3be)

You'll notice here that the cronjob is setup to run every second ( * * * * *).
this is because the script in that file location is just a test.

when we move to the PI the cronjob will need updating to (0 5 * * *).

0: Specifies the 0th minute of the hour.

5: Specifies the 5th hour of the day (which is 5 AM).

*: Specifies every day of the month.

*: Specifies every month.

*: Specifies every day of the week.

which will run the script every days at 05 am.













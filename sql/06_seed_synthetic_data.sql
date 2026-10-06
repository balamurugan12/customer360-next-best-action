USE DATABASE CUSTOMER360_HACKATHON;
USE SCHEMA APP;

MERGE INTO CUSTOMERS target
USING (
  SELECT column1 AS CUSTOMER_ID, column2 AS NAME, column3 AS SEGMENT, column4 AS CITY,
         column5 AS INDUSTRY, column6 AS TENURE_YEARS, column7 AS PRODUCT_COUNT,
         column8 AS ANNUAL_VALUE
  FROM VALUES
    ('C1001','Aarav Mehta','Premium','Mumbai','Insurance',6.2,4,220000),
    ('C1002','Diya Nair','Mass Affluent','Bengaluru','Lending',2.1,2,98000),
    ('C1003','Vikram Rao','Premium','Hyderabad','Insurance',4.8,3,175000),
    ('C1004','Meera Iyer','Emerging','Pune','Lending',1.4,1,42000),
    ('C1005','Kabir Sharma','Mass Affluent','Delhi','Insurance',3.5,2,115000),
    ('C1006','Ananya Gupta','Premium','Chennai','Lending',7.1,5,310000),
    ('C1007','Rohan Das','Emerging','Kolkata','Insurance',0.9,1,36000),
    ('C1008','Nisha Menon','Mass Affluent','Kochi','Lending',2.9,2,89000),
    ('C1009','Arjun Kapoor','Premium','Gurugram','Insurance',5.4,4,260000),
    ('C1010','Sara Khan','Mass Affluent','Jaipur','Lending',3.1,3,104000)
) source
ON target.CUSTOMER_ID = source.CUSTOMER_ID
WHEN NOT MATCHED THEN INSERT
  (CUSTOMER_ID, NAME, SEGMENT, CITY, INDUSTRY, TENURE_YEARS, PRODUCT_COUNT, ANNUAL_VALUE)
  VALUES (source.CUSTOMER_ID, source.NAME, source.SEGMENT, source.CITY, source.INDUSTRY,
          source.TENURE_YEARS, source.PRODUCT_COUNT, source.ANNUAL_VALUE);

MERGE INTO ACCOUNTS target
USING (
  SELECT column1 AS ACCOUNT_ID, column2 AS CUSTOMER_ID, column3 AS PRODUCT_TYPE,
         column4 AS STATUS, column5 AS BALANCE_OR_COVER, column6 AS OPENED_DATE
  FROM VALUES
    ('A9001','C1001','Health Insurance','Active',1500000,'2020-04-12'),
    ('A9002','C1001','Term Insurance','Active',5000000,'2021-01-22'),
    ('A9003','C1002','Personal Loan','Active',420000,'2025-02-18'),
    ('A9004','C1003','Motor Insurance','Active',900000,'2022-08-05'),
    ('A9005','C1004','Personal Loan','Active',180000,'2026-01-20'),
    ('A9006','C1005','Health Insurance','Active',700000,'2023-09-11'),
    ('A9007','C1006','Home Loan','Active',5600000,'2019-05-06'),
    ('A9008','C1006','Wealth Plan','Active',1200000,'2021-10-16'),
    ('A9009','C1007','Motor Insurance','Active',450000,'2026-03-09'),
    ('A9010','C1008','Personal Loan','Active',320000,'2024-04-25'),
    ('A9011','C1009','Health Insurance','Active',2000000,'2020-07-30'),
    ('A9012','C1010','Credit Line','Active',260000,'2023-12-14')
) source
ON target.ACCOUNT_ID = source.ACCOUNT_ID
WHEN NOT MATCHED THEN INSERT
  (ACCOUNT_ID, CUSTOMER_ID, PRODUCT_TYPE, STATUS, BALANCE_OR_COVER, OPENED_DATE)
  VALUES (source.ACCOUNT_ID, source.CUSTOMER_ID, source.PRODUCT_TYPE, source.STATUS,
          source.BALANCE_OR_COVER, source.OPENED_DATE);

MERGE INTO INTERACTIONS target
USING (
  SELECT column1 AS INTERACTION_ID, column2 AS CUSTOMER_ID, column3 AS CHANNEL,
         column4 AS INTERACTION_DATE, column5 AS ISSUE_TYPE, column6 AS SENTIMENT,
         column7 AS STATUS, column8 AS TRANSCRIPT
  FROM VALUES
    ('I5001','C1001','Call','2026-09-22','Claim Delay','Negative','Open','Customer said the hospital claim has been pending for three weeks and asked for a clear timeline. They are unhappy because support promised a callback twice.'),
    ('I5002','C1001','Email','2026-09-15','Service Request','Neutral','Closed','Customer requested policy document copy and nominee update confirmation.'),
    ('I5003','C1002','Call','2026-09-25','Billing','Negative','Open','Customer reported that an EMI was debited twice and requested urgent reversal before the next billing cycle.'),
    ('I5004','C1003','Call','2026-09-18','Renewal','Positive','Closed','Customer asked about renewal benefits and appreciated the no-claim bonus explanation.'),
    ('I5005','C1004','Chat','2026-09-29','General','Neutral','Closed','Customer asked for repayment schedule and prepayment charges.'),
    ('I5006','C1005','Call','2026-09-20','Complaint','Negative','Open','Customer complained about repeated document requests for the same health policy endorsement.'),
    ('I5007','C1006','Email','2026-09-28','General','Positive','Closed','Customer requested investment statement and thanked the advisor for quick help.'),
    ('I5008','C1007','Call','2026-09-26','Billing','Negative','Open','Customer said premium payment succeeded but the policy still shows unpaid in the app.'),
    ('I5009','C1008','Chat','2026-09-16','Service Request','Neutral','Closed','Customer asked for address change and updated employment details.'),
    ('I5010','C1009','Call','2026-09-30','Claim Delay','Negative','Open','Customer escalated a reimbursement claim delay and said they may switch providers if not resolved.'),
    ('I5011','C1010','Email','2026-09-12','Renewal','Positive','Closed','Customer asked for credit line renewal options and showed interest in higher limit.')
) source
ON target.INTERACTION_ID = source.INTERACTION_ID
WHEN NOT MATCHED THEN INSERT
  (INTERACTION_ID, CUSTOMER_ID, CHANNEL, INTERACTION_DATE, ISSUE_TYPE, SENTIMENT, STATUS, TRANSCRIPT)
  VALUES (source.INTERACTION_ID, source.CUSTOMER_ID, source.CHANNEL, source.INTERACTION_DATE,
          source.ISSUE_TYPE, source.SENTIMENT, source.STATUS, source.TRANSCRIPT);

USE DATABASE CUSTOMER360_HACKATHON;
USE SCHEMA APP;

-- First-run enrichment example. Cortex model calls can consume credits.
-- IF NOT EXISTS prevents reruns from replacing the table and repeating inference.
CREATE TABLE IF NOT EXISTS INTERACTION_AI_ENRICHED AS
SELECT
  INTERACTION_ID,
  CUSTOMER_ID,
  CHANNEL,
  INTERACTION_DATE,
  ISSUE_TYPE,
  STATUS,
  TRANSCRIPT,
  SNOWFLAKE.CORTEX.SUMMARIZE(TRANSCRIPT) AS AI_SUMMARY,
  SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
    TRANSCRIPT,
    ['Positive', 'Neutral', 'Negative']
  ) AS AI_SENTIMENT,
  SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'Recommend one operational next step for this customer interaction in one sentence: ' || TRANSCRIPT
  ) AS AI_RECOMMENDED_STEP
FROM INTERACTIONS;

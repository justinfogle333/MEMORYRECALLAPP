# V8 Project Corpus Extraction Summary

Generated: 2026-05-09T02:25:57.930156+00:00

| Metric | Count |
|---|---:|
| ZIP archives processed | 8 |
| Unique files organized | 265 |
| Duplicate files removed | 206 |
| Sensitive/private files excluded | 8 |

## Organized File Counts

| Category | Files |
|---|---:|
| `01_code_and_config` | 171 |
| `02_docs_and_strategy` | 51 |
| `03_data_and_spreadsheets` | 7 |
| `04_media_assets` | 23 |
| `05_nested_archives` | 3 |
| `06_other_assets` | 10 |

## ZIP Archive Inputs

| Archive | Size Bytes | Extracted Members | Errors |
|---|---:|---:|---:|
| `Global_Sales_Force__01_Project_Management__docs__Developing_AI_Driven_Marketing_Strategies_for_Lead_Generation.zip` | 34427174 | 70 | 0 |
| `Global_Sales_Force__01_Project_Management__docs__Global_Sales_Force.zip` | 710178 | 53 | 0 |
| `Global_Sales_Force__01_Project_Management__docs__Global_Sales_Force_FULL_EXPORT.zip` | 15208928 | 182 | 0 |
| `Global_Sales_Force__03_Automated_Review_Agent__src__review_agent.zip` | 22280 | 13 | 0 |
| `Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2.zip` | 2266443 | 17 | 0 |
| `Global_Sales_Force__Logistical_Questionnaire__MOVE_INTELLIGENCE_FULL_SUITE.zip` | 27515330 | 109 | 0 |
| `bot_a_lead_quoting_engine_v3.zip` | 2288458 | 22 | 0 |
| `drive_id_1inM9__code__review_agent.zip` | 22280 | 13 | 0 |

## Notes

Original ZIP files were retained only in local staging and were not placed in the Git corpus to reduce redundancy. The extracted unique files and manifests are the recall-optimized source of truth.

## Nested Archive Handling

Three nested ZIP files were discovered inside the marketing-strategy export. They were not retained as compressed files because the same archives were already processed as top-level inputs during this V8 pass. Their paths are recorded in `manifests/v8_nested_archives_removed.txt`, and their extracted contents remain available through the organized corpus.

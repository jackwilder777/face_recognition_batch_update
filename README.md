# Batch updater
Batch updating face recognition bot

## Setup
The following credentials are required to run test cases on this bot. Please read `https://core.telegram.org/api/obtaining_api_id` for instruction to generate API credentials.
- Telegram account session `user.session`
- API credentials `credential.py`
    - Example:
    ```
    api_id = 123456
    api_hash = 'abcdefg123456'
    ```
Use the script `create_session.py` with the above API credentials to generate the session file.
- Target bot's id in `main.py` BOT_ID

## Target Folder structure
```
Folder>
    subjectA.png
    subjectA_1.png
    subjectA_2.png
    subjectB.png
    subjectC.png
```
If there's more than one photo of the same face, add _N postfix to indicate.

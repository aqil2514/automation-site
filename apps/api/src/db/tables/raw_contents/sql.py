INSERT_NEW_RAW_CONTENTS = """
INSERT INTO raw_contents (
    source_url,
    title,
    content_raw,
    image_url,
    status
)
VALUES ($1, $2, $3, $4, $5)
"""

SELECT_RAW_CONTENTS = """
SELECT 
    *
FROM raw_contents
ORDER BY created_at DESC
"""

SELECT_RAW_CONTENTS_BY_STATUS = """
SELECT * FROM raw_contents 
WHERE status = $1 
ORDER BY created_at DESC
"""

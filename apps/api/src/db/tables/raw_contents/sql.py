INSERT_NEW_RAW_CONTENTS="""
INSERT INTO raw_contents (
    source_url,
    title,
    content_raw,
    image_url,
    status
)
VALUES ($1, $2, $3, $4, $5)
"""
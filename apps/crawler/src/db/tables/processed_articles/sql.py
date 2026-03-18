SELECT_APPROVED_ARTICLE = """
SELECT
    *
FROM processed_articles
WHERE status = 'approved'
LIMIT 1
"""

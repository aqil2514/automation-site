INSERT_PROCESSED_ARTICLE = """
INSERT INTO processed_articles (
    id, raw_content_id, title, slug, content_full, excerpt, tags, image_url, status
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
RETURNING id
"""

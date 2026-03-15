INSERT_ARTICLE_POSTING = """
INSERT INTO article_postings (
    article_id, platform_name, status
) VALUES ($1, $2, $3)
"""

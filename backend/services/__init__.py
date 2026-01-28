"""
Services package initialization
"""
from .meilisearch_service import MeilisearchService
from .project_service import ProjectService

__all__ = ["MeilisearchService", "ProjectService"]

"""
Meilisearch client service for interacting with Meilisearch instances
"""
import meilisearch
from typing import Optional, Dict, Any, List


def _snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase"""
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def _to_dict(obj: Any, convert_keys: bool = True) -> Any:
    """Convert Meilisearch objects to JSON-serializable dictionaries"""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        if convert_keys:
            return {_snake_to_camel(k): _to_dict(v, convert_keys) for k, v in obj.items()}
        return {k: _to_dict(v, convert_keys) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_dict(item, convert_keys) for item in obj]
    if hasattr(obj, '__dict__'):
        if convert_keys:
            return {_snake_to_camel(k): _to_dict(v, convert_keys) for k, v in obj.__dict__.items() if not k.startswith('_')}
        return {k: _to_dict(v, convert_keys) for k, v in obj.__dict__.items() if not k.startswith('_')}
    # Fallback for other types
    return obj


class MeilisearchService:
    """Service class for Meilisearch API interactions"""
    
    def __init__(self, url: str, api_key: str = None):
        """
        Initialize Meilisearch client
        
        Args:
            url: Meilisearch instance URL
            api_key: Master API key (optional)
        """
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.client = meilisearch.Client(self.url, self.api_key)
    
    # ==================== Health & Stats ====================
    
    def health(self) -> Dict[str, Any]:
        """Check Meilisearch instance health"""
        return self.client.health()
    
    def is_healthy(self) -> bool:
        """Check if Meilisearch instance is healthy"""
        return self.client.is_healthy()
    
    def get_version(self) -> Dict[str, str]:
        """Get Meilisearch version information"""
        return self.client.get_version()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get global stats for the instance"""
        return self.client.get_all_stats()
    
    # ==================== Index Management ====================
    
    def get_indexes(self) -> List[Dict[str, Any]]:
        """Get all indexes"""
        result = self.client.get_indexes()
        return [{"uid": idx.uid, "primaryKey": idx.primary_key, 
                 "createdAt": idx.created_at, "updatedAt": idx.updated_at}
                for idx in result.get("results", [])]
    
    def get_index(self, uid: str):
        """Get a specific index"""
        return self.client.get_index(uid)
    
    def create_index(self, uid: str, primary_key: str = None) -> Dict[str, Any]:
        """Create a new index"""
        options = {"primaryKey": primary_key} if primary_key else {}
        task = self.client.create_index(uid, options)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def delete_index(self, uid: str) -> Dict[str, Any]:
        """Delete an index"""
        task = self.client.delete_index(uid)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_index_stats(self, uid: str) -> Dict[str, Any]:
        """Get stats for a specific index"""
        index = self.client.index(uid)
        stats = index.get_stats()
        # Convert stats object to dict for JSON serialization
        return _to_dict(stats)
    
    # ==================== Document Management ====================
    
    def get_documents(self, uid: str, offset: int = 0, limit: int = 20, 
                      fields: List[str] = None) -> Dict[str, Any]:
        """Get documents from an index"""
        index = self.client.index(uid)
        params = {"offset": offset, "limit": limit}
        if fields:
            params["fields"] = fields
        return index.get_documents(params)
    
    def get_document(self, uid: str, document_id: str) -> Dict[str, Any]:
        """Get a specific document"""
        index = self.client.index(uid)
        return index.get_document(document_id)
    
    def add_documents(self, uid: str, documents: List[Dict], 
                      primary_key: str = None) -> Dict[str, Any]:
        """Add or update documents"""
        index = self.client.index(uid)
        task = index.add_documents(documents, primary_key)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def update_documents(self, uid: str, documents: List[Dict],
                         primary_key: str = None) -> Dict[str, Any]:
        """Update documents"""
        index = self.client.index(uid)
        task = index.update_documents(documents, primary_key)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def delete_document(self, uid: str, document_id: str) -> Dict[str, Any]:
        """Delete a specific document"""
        index = self.client.index(uid)
        task = index.delete_document(document_id)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def delete_documents(self, uid: str, document_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple documents"""
        index = self.client.index(uid)
        task = index.delete_documents(document_ids)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def delete_all_documents(self, uid: str) -> Dict[str, Any]:
        """Delete all documents from an index"""
        index = self.client.index(uid)
        task = index.delete_all_documents()
        return {"taskUid": task.task_uid, "status": task.status}
    
    # ==================== Search ====================
    
    def search(self, uid: str, query: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search documents in an index"""
        index = self.client.index(uid)
        search_params = params or {}
        return index.search(query, search_params)
    
    # ==================== Settings ====================
    
    def get_settings(self, uid: str) -> Dict[str, Any]:
        """Get all settings for an index"""
        index = self.client.index(uid)
        settings = index.get_settings()
        # Convert any non-serializable objects to dicts
        return _to_dict(settings)
    
    def update_settings(self, uid: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update settings for an index"""
        index = self.client.index(uid)
        task = index.update_settings(settings)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def reset_settings(self, uid: str) -> Dict[str, Any]:
        """Reset settings to default"""
        index = self.client.index(uid)
        task = index.reset_settings()
        return {"taskUid": task.task_uid, "status": task.status}
    
    # Individual settings
    def get_searchable_attributes(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_searchable_attributes()
    
    def update_searchable_attributes(self, uid: str, attrs: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_searchable_attributes(attrs)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_displayed_attributes(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_displayed_attributes()
    
    def update_displayed_attributes(self, uid: str, attrs: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_displayed_attributes(attrs)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_filterable_attributes(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_filterable_attributes()
    
    def update_filterable_attributes(self, uid: str, attrs: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_filterable_attributes(attrs)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_sortable_attributes(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_sortable_attributes()
    
    def update_sortable_attributes(self, uid: str, attrs: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_sortable_attributes(attrs)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_ranking_rules(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_ranking_rules()
    
    def update_ranking_rules(self, uid: str, rules: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_ranking_rules(rules)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_synonyms(self, uid: str) -> Dict[str, List[str]]:
        index = self.client.index(uid)
        return index.get_synonyms()
    
    def update_synonyms(self, uid: str, synonyms: Dict[str, List[str]]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_synonyms(synonyms)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_stop_words(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_stop_words()
    
    def update_stop_words(self, uid: str, stop_words: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_stop_words(stop_words)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_typo_tolerance(self, uid: str) -> Dict[str, Any]:
        index = self.client.index(uid)
        return index.get_typo_tolerance()
    
    def update_typo_tolerance(self, uid: str, typo_tolerance: Dict[str, Any]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_typo_tolerance(typo_tolerance)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_pagination(self, uid: str) -> Dict[str, int]:
        index = self.client.index(uid)
        return index.get_pagination()
    
    def update_pagination(self, uid: str, pagination: Dict[str, int]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_pagination(pagination)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_faceting(self, uid: str) -> Dict[str, Any]:
        index = self.client.index(uid)
        return index.get_faceting()
    
    def update_faceting(self, uid: str, faceting: Dict[str, Any]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_faceting(faceting)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_dictionary(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_dictionary()
    
    def update_dictionary(self, uid: str, dictionary: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_dictionary(dictionary)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_separator_tokens(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_separator_tokens()
    
    def update_separator_tokens(self, uid: str, tokens: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_separator_tokens(tokens)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def get_non_separator_tokens(self, uid: str) -> List[str]:
        index = self.client.index(uid)
        return index.get_non_separator_tokens()
    
    def update_non_separator_tokens(self, uid: str, tokens: List[str]) -> Dict[str, Any]:
        index = self.client.index(uid)
        task = index.update_non_separator_tokens(tokens)
        return {"taskUid": task.task_uid, "status": task.status}
    
    # ==================== Tasks ====================
    
    def get_tasks(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get tasks with optional filters"""
        result = self.client.get_tasks(params)
        return _to_dict(result)
    
    def get_task(self, task_uid: int) -> Dict[str, Any]:
        """Get a specific task"""
        result = self.client.get_task(task_uid)
        return _to_dict(result)
    
    def cancel_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel tasks matching the filters"""
        task = self.client.cancel_tasks(params)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def delete_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Delete tasks matching the filters"""
        task = self.client.delete_tasks(params)
        return {"taskUid": task.task_uid, "status": task.status}
    
    def wait_for_task(self, task_uid: int, timeout_in_ms: int = 5000) -> Dict[str, Any]:
        """Wait for a task to complete"""
        return self.client.wait_for_task(task_uid, timeout_in_ms)
    
    # ==================== Keys ====================
    
    def get_keys(self) -> Dict[str, Any]:
        """Get all API keys"""
        result = self.client.get_keys()
        return _to_dict(result)
    
    def get_key(self, key: str) -> Dict[str, Any]:
        """Get a specific API key"""
        result = self.client.get_key(key)
        return _to_dict(result)
    
    def create_key(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new API key"""
        result = self.client.create_key(options)
        return _to_dict(result)
    
    def update_key(self, key: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Update an API key"""
        result = self.client.update_key(key, options)
        return _to_dict(result)
    
    def delete_key(self, key: str) -> int:
        """Delete an API key"""
        return self.client.delete_key(key)
    
    # ==================== Dumps ====================
    
    def create_dump(self) -> Dict[str, Any]:
        """Create a database dump"""
        task = self.client.create_dump()
        return {"taskUid": task.task_uid, "status": task.status}
    
    # ==================== Snapshots ====================
    
    def create_snapshot(self) -> Dict[str, Any]:
        """Create a database snapshot"""
        task = self.client.create_snapshot()
        return {"taskUid": task.task_uid, "status": task.status}

"""
Project service for managing project CRUD operations
"""
from typing import List, Optional, Dict, Any
from backend.models import db, Project
from backend.services.meilisearch_service import MeilisearchService


class ProjectService:
    """Service for project management operations"""
    
    def __init__(self):
        self.session = db.session
    
    def get_all(self, include_inactive: bool = False) -> List[Project]:
        """Get all projects"""
        query = self.session.query(Project)
        if not include_inactive:
            query = query.filter(Project.is_active == True)
        return query.order_by(Project.created_at.desc()).all()
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return self.session.query(Project).filter(Project.id == project_id).first()
    
    def create(self, name: str, url: str, api_key: str = None, 
               description: str = None) -> Project:
        """Create a new project"""
        project = Project(
            name=name,
            url=url.rstrip("/"),
            api_key=api_key,
            description=description,
        )
        self.session.add(project)
        self.session.commit()
        return project
    
    def update(self, project_id: int, **kwargs) -> Optional[Project]:
        """Update a project"""
        project = self.get_by_id(project_id)
        if not project:
            return None
        
        for key, value in kwargs.items():
            if hasattr(project, key) and value is not None:
                if key == "url":
                    value = value.rstrip("/")
                setattr(project, key, value)
        
        self.session.commit()
        return project
    
    def delete(self, project_id: int) -> bool:
        """Delete a project (soft delete)"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        project.is_active = False
        self.session.commit()
        return True
    
    def hard_delete(self, project_id: int) -> bool:
        """Permanently delete a project"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        self.session.delete(project)
        self.session.commit()
        return True
    
    def get_meilisearch_client(self, project_id: int) -> Optional[MeilisearchService]:
        """Get MeilisearchService instance for a project"""
        project = self.get_by_id(project_id)
        if not project:
            return None
        return MeilisearchService(project.url, project.api_key)
    
    def test_connection(self, url: str, api_key: str = None) -> Dict[str, Any]:
        """Test connection to a Meilisearch instance"""
        try:
            service = MeilisearchService(url, api_key)
            if service.is_healthy():
                version = service.get_version()
                stats = service.get_stats()
                return {
                    "success": True,
                    "version": version,
                    "stats": stats,
                }
            else:
                return {"success": False, "error": "Instance is not healthy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_project_stats(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get stats for a project's Meilisearch instance"""
        service = self.get_meilisearch_client(project_id)
        if not service:
            return None
        
        try:
            stats = service.get_stats()
            version = service.get_version()
            return {
                "version": version,
                "stats": stats,
                "healthy": service.is_healthy(),
            }
        except Exception as e:
            return {"error": str(e), "healthy": False}
    
    def get_experimental_features(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get experimental features status for a project's Meilisearch instance"""
        service = self.get_meilisearch_client(project_id)
        if not service:
            return None
        
        try:
            # 直接调用Meilisearch的experimental-features API
            import requests
            headers = {}
            if service.api_key:
                headers["Authorization"] = f"Bearer {service.api_key}"
            
            response = requests.get(
                f"{service.url}/experimental-features",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def update_experimental_features(self, project_id: int, features: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update experimental features for a project's Meilisearch instance"""
        service = self.get_meilisearch_client(project_id)
        if not service:
            return None
        
        try:
            # 直接调用Meilisearch的experimental-features API
            import requests
            headers = {
                "Content-Type": "application/json"
            }
            if service.api_key:
                headers["Authorization"] = f"Bearer {service.api_key}"
            
            response = requests.patch(
                f"{service.url}/experimental-features",
                json=features,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

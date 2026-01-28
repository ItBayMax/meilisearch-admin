"""
API Keys management endpoints
"""
from flask import Blueprint, request, jsonify
from backend.services import ProjectService

key_bp = Blueprint("keys", __name__, url_prefix="/api/projects/<int:project_id>/keys")
project_service = ProjectService()


def get_meilisearch_service(project_id):
    """Helper to get MeilisearchService for a project"""
    return project_service.get_meilisearch_client(project_id)


@key_bp.route("", methods=["GET"])
def get_keys(project_id):
    """Get all API keys"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        result = service.get_keys()
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@key_bp.route("/<string:key>", methods=["GET"])
def get_key(project_id, key):
    """Get a specific API key"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        result = service.get_key(key)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@key_bp.route("", methods=["POST"])
def create_key(project_id):
    """Create a new API key"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get("actions"):
        return jsonify({"success": False, "error": "Actions are required"}), 400
    if not data.get("indexes"):
        return jsonify({"success": False, "error": "Indexes are required"}), 400
    
    options = {
        "actions": data["actions"],
        "indexes": data["indexes"],
    }
    
    if data.get("name"):
        options["name"] = data["name"]
    if data.get("description"):
        options["description"] = data["description"]
    if data.get("uid"):
        options["uid"] = data["uid"]
    if data.get("expiresAt"):
        options["expiresAt"] = data["expiresAt"]
    
    try:
        result = service.create_key(options)
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@key_bp.route("/<string:key>", methods=["PATCH"])
def update_key(project_id, key):
    """Update an API key"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    options = {}
    
    if data.get("name") is not None:
        options["name"] = data["name"]
    if data.get("description") is not None:
        options["description"] = data["description"]
    
    try:
        result = service.update_key(key, options)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@key_bp.route("/<string:key>", methods=["DELETE"])
def delete_key(project_id, key):
    """Delete an API key"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        service.delete_key(key)
        return jsonify({"success": True, "message": "Key deleted"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

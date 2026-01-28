"""
Project API endpoints
"""
from flask import Blueprint, request, jsonify
from backend.services import ProjectService

project_bp = Blueprint("projects", __name__, url_prefix="/api/projects")
project_service = ProjectService()


@project_bp.route("", methods=["GET"])
def get_projects():
    """Get all projects"""
    include_inactive = request.args.get("include_inactive", "false").lower() == "true"
    projects = project_service.get_all(include_inactive=include_inactive)
    return jsonify({
        "success": True,
        "data": [p.to_dict() for p in projects],
    })


@project_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Get a specific project"""
    project = project_service.get_by_id(project_id)
    if not project:
        return jsonify({"success": False, "error": "Project not found"}), 404
    return jsonify({"success": True, "data": project.to_dict()})


@project_bp.route("", methods=["POST"])
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    if not data.get("name") or not data.get("url"):
        return jsonify({"success": False, "error": "Name and URL are required"}), 400
    
    project = project_service.create(
        name=data["name"],
        url=data["url"],
        api_key=data.get("api_key"),
        description=data.get("description"),
    )
    return jsonify({"success": True, "data": project.to_dict()}), 201


@project_bp.route("/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    """Update a project"""
    data = request.get_json()
    project = project_service.update(
        project_id,
        name=data.get("name"),
        url=data.get("url"),
        api_key=data.get("api_key"),
        description=data.get("description"),
    )
    if not project:
        return jsonify({"success": False, "error": "Project not found"}), 404
    return jsonify({"success": True, "data": project.to_dict()})


@project_bp.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project"""
    hard_delete = request.args.get("hard", "false").lower() == "true"
    if hard_delete:
        success = project_service.hard_delete(project_id)
    else:
        success = project_service.delete(project_id)
    
    if not success:
        return jsonify({"success": False, "error": "Project not found"}), 404
    return jsonify({"success": True, "message": "Project deleted"})


@project_bp.route("/test-connection", methods=["POST"])
def test_connection():
    """Test connection to a Meilisearch instance"""
    data = request.get_json()
    if not data.get("url"):
        return jsonify({"success": False, "error": "URL is required"}), 400
    
    result = project_service.test_connection(
        url=data["url"],
        api_key=data.get("api_key"),
    )
    return jsonify(result)


@project_bp.route("/<int:project_id>/stats", methods=["GET"])
def get_project_stats(project_id):
    """Get stats for a project's Meilisearch instance"""
    stats = project_service.get_project_stats(project_id)
    if stats is None:
        return jsonify({"success": False, "error": "Project not found"}), 404
    return jsonify({"success": True, "data": stats})

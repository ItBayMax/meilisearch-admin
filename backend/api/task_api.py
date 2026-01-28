"""
Task API endpoints
"""
from flask import Blueprint, request, jsonify
from backend.services import ProjectService

task_bp = Blueprint("tasks", __name__, url_prefix="/api/projects/<int:project_id>/tasks")
project_service = ProjectService()


def get_meilisearch_service(project_id):
    """Helper to get MeilisearchService for a project"""
    return project_service.get_meilisearch_client(project_id)


@task_bp.route("", methods=["GET"])
def get_tasks(project_id):
    """Get tasks with optional filters"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    # Build filter params
    params = {}
    
    # Pagination
    limit = request.args.get("limit", type=int)
    offset = request.args.get("from", type=int)
    if limit:
        params["limit"] = limit
    if offset:
        params["from"] = offset
    
    # Filter by status
    statuses = request.args.get("statuses")
    if statuses:
        params["statuses"] = statuses.split(",")
    
    # Filter by type
    types = request.args.get("types")
    if types:
        params["types"] = types.split(",")
    
    # Filter by index
    index_uids = request.args.get("indexUids")
    if index_uids:
        params["indexUids"] = index_uids.split(",")
    
    # Filter by UID
    uids = request.args.get("uids")
    if uids:
        params["uids"] = [int(uid) for uid in uids.split(",")]
    
    # Filter by date
    before_enqueued_at = request.args.get("beforeEnqueuedAt")
    after_enqueued_at = request.args.get("afterEnqueuedAt")
    before_started_at = request.args.get("beforeStartedAt")
    after_started_at = request.args.get("afterStartedAt")
    before_finished_at = request.args.get("beforeFinishedAt")
    after_finished_at = request.args.get("afterFinishedAt")
    
    if before_enqueued_at:
        params["beforeEnqueuedAt"] = before_enqueued_at
    if after_enqueued_at:
        params["afterEnqueuedAt"] = after_enqueued_at
    if before_started_at:
        params["beforeStartedAt"] = before_started_at
    if after_started_at:
        params["afterStartedAt"] = after_started_at
    if before_finished_at:
        params["beforeFinishedAt"] = before_finished_at
    if after_finished_at:
        params["afterFinishedAt"] = after_finished_at
    
    try:
        result = service.get_tasks(params if params else None)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@task_bp.route("/<int:task_uid>", methods=["GET"])
def get_task(project_id, task_uid):
    """Get a specific task"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        task = service.get_task(task_uid)
        return jsonify({"success": True, "data": task})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@task_bp.route("/cancel", methods=["POST"])
def cancel_tasks(project_id):
    """Cancel tasks matching filters"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    params = {}
    
    if data.get("uids"):
        params["uids"] = data["uids"]
    if data.get("statuses"):
        params["statuses"] = data["statuses"]
    if data.get("types"):
        params["types"] = data["types"]
    if data.get("indexUids"):
        params["indexUids"] = data["indexUids"]
    
    if not params:
        return jsonify({"success": False, "error": "At least one filter is required"}), 400
    
    try:
        result = service.cancel_tasks(params)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@task_bp.route("", methods=["DELETE"])
def delete_tasks(project_id):
    """Delete tasks matching filters"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    params = {}
    
    if data.get("uids"):
        params["uids"] = data["uids"]
    if data.get("statuses"):
        params["statuses"] = data["statuses"]
    if data.get("types"):
        params["types"] = data["types"]
    if data.get("indexUids"):
        params["indexUids"] = data["indexUids"]
    
    if not params:
        return jsonify({"success": False, "error": "At least one filter is required"}), 400
    
    try:
        result = service.delete_tasks(params)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@task_bp.route("/<int:task_uid>/wait", methods=["POST"])
def wait_for_task(project_id, task_uid):
    """Wait for a task to complete"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json() or {}
    timeout = data.get("timeout", 5000)
    
    try:
        result = service.wait_for_task(task_uid, timeout)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

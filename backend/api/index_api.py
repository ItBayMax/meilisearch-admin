"""
Index API endpoints
"""
import json
import requests as http_requests
from flask import Blueprint, request, jsonify
from backend.services import ProjectService

index_bp = Blueprint("indexes", __name__, url_prefix="/api/projects/<int:project_id>/indexes")
project_service = ProjectService()


def get_meilisearch_service(project_id):
    """Helper to get MeilisearchService for a project"""
    return project_service.get_meilisearch_client(project_id)


@index_bp.route("", methods=["GET"])
def get_indexes(project_id):
    """Get all indexes for a project"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        indexes = service.get_indexes()
        return jsonify({"success": True, "data": indexes})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>", methods=["GET"])
def get_index(project_id, uid):
    """Get a specific index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        index = service.get_index(uid)
        stats = service.get_index_stats(uid)
        return jsonify({
            "success": True,
            "data": {
                "uid": index.uid,
                "primaryKey": index.primary_key,
                "createdAt": index.created_at,
                "updatedAt": index.updated_at,
                "stats": stats,
            }
        })
    except Exception as e:
        error_msg = str(e)
        print(f"Error fetching index {uid} for project {project_id}: {error_msg}")
        # Check if it's an index not found error
        if "index_not_found" in error_msg.lower() or "not found" in error_msg.lower():
            return jsonify({"success": False, "error": f"Index '{uid}' not found"}), 404
        return jsonify({"success": False, "error": error_msg}), 500


@index_bp.route("", methods=["POST"])
def create_index(project_id):
    """Create a new index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    if not data.get("uid"):
        return jsonify({"success": False, "error": "Index UID is required"}), 400
    
    try:
        result = service.create_index(data["uid"], data.get("primaryKey"))
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>", methods=["DELETE"])
def delete_index(project_id, uid):
    """Delete an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        result = service.delete_index(uid)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/stats", methods=["GET"])
def get_index_stats(project_id, uid):
    """Get stats for an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        stats = service.get_index_stats(uid)
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== Documents ====================

@index_bp.route("/<string:uid>/documents", methods=["GET"])
def get_documents(project_id, uid):
    """Get documents from an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    offset = request.args.get("offset", 0, type=int)
    limit = request.args.get("limit", 20, type=int)
    fields = request.args.get("fields")
    fields_list = fields.split(",") if fields else None
    
    try:
        result = service.get_documents(uid, offset, limit, fields_list)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/documents/<string:doc_id>", methods=["GET"])
def get_document(project_id, uid, doc_id):
    """Get a specific document"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        document = service.get_document(uid, doc_id)
        return jsonify({"success": True, "data": document})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/documents", methods=["POST"])
def add_documents(project_id, uid):
    """Add documents to an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    documents = data.get("documents", [])
    primary_key = data.get("primaryKey")
    
    if not documents:
        return jsonify({"success": False, "error": "Documents are required"}), 400
    
    try:
        result = service.add_documents(uid, documents, primary_key)
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/documents/upload", methods=["POST"])
def upload_documents_file(project_id, uid):
    """Add documents by uploading a JSON or CSV file"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404

    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "error": "No file provided"}), 400

    primary_key = request.form.get("primaryKey")
    filename = file.filename.lower()

    try:
        if filename.endswith(".json"):
            content = file.read().decode("utf-8")
            documents = json.loads(content)
            if isinstance(documents, dict):
                documents = [documents]
        elif filename.endswith(".csv"):
            import csv
            import io
            content = file.read().decode("utf-8")
            reader = csv.DictReader(io.StringIO(content))
            documents = [row for row in reader]
        else:
            return jsonify({"success": False, "error": "Unsupported file format. Only .json and .csv are supported."}), 400

        if not documents:
            return jsonify({"success": False, "error": "File contains no documents"}), 400

        result = service.add_documents(uid, documents, primary_key if primary_key else None)
        return jsonify({"success": True, "data": result, "count": len(documents)}), 201
    except json.JSONDecodeError:
        return jsonify({"success": False, "error": "Invalid JSON file format"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/documents/fetch-url", methods=["POST"])
def fetch_documents_from_url(project_id, uid):
    """Add documents by fetching from a remote URL and extracting a specific field"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404

    data = request.get_json()
    url = data.get("url")
    field_path = data.get("fieldPath", "")  # e.g. "data.items" or "results"
    primary_key = data.get("primaryKey")
    headers = data.get("headers", {})  # optional custom headers

    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400

    try:
        resp = http_requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        body = resp.json()

        # Extract documents from response using field_path
        documents = body
        if field_path:
            for key in field_path.split("."):
                key = key.strip()
                if isinstance(documents, dict) and key in documents:
                    documents = documents[key]
                elif isinstance(documents, list) and key.isdigit():
                    documents = documents[int(key)]
                else:
                    return jsonify({"success": False, "error": f"Field path '{field_path}' not found in response"}), 400

        if isinstance(documents, dict):
            documents = [documents]

        if not isinstance(documents, list):
            return jsonify({"success": False, "error": "Extracted data is not a list of documents"}), 400

        if not documents:
            return jsonify({"success": False, "error": "No documents found at the specified field path"}), 400

        result = service.add_documents(uid, documents, primary_key if primary_key else None)
        return jsonify({"success": True, "data": result, "count": len(documents)}), 201
    except http_requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Request timed out"}), 504
    except http_requests.exceptions.ConnectionError:
        return jsonify({"success": False, "error": "Failed to connect to the URL"}), 502
    except http_requests.exceptions.HTTPError as e:
        return jsonify({"success": False, "error": f"HTTP error: {e.response.status_code}"}), 502
    except json.JSONDecodeError:
        return jsonify({"success": False, "error": "Response is not valid JSON"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/documents/<string:doc_id>", methods=["DELETE"])
def delete_document(project_id, uid, doc_id):
    """Delete a document"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        result = service.delete_document(uid, doc_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/documents", methods=["DELETE"])
def delete_documents(project_id, uid):
    """Delete multiple documents"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    
    if data and data.get("ids"):
        # Delete specific documents
        try:
            result = service.delete_documents(uid, data["ids"])
            return jsonify({"success": True, "data": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        # Delete all documents
        try:
            result = service.delete_all_documents(uid)
            return jsonify({"success": True, "data": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


# ==================== Search ====================

@index_bp.route("/<string:uid>/search", methods=["POST"])
def search(project_id, uid):
    """Search documents in an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    query = data.get("q", "")
    
    search_params = {}
    if "limit" in data:
        search_params["limit"] = data["limit"]
    if "offset" in data:
        search_params["offset"] = data["offset"]
    if "filter" in data:
        search_params["filter"] = data["filter"]
    if "sort" in data:
        search_params["sort"] = data["sort"]
    if "facets" in data:
        search_params["facets"] = data["facets"]
    if "attributesToRetrieve" in data:
        search_params["attributesToRetrieve"] = data["attributesToRetrieve"]
    if "attributesToHighlight" in data:
        search_params["attributesToHighlight"] = data["attributesToHighlight"]
    if "showRankingScore" in data:
        search_params["showRankingScore"] = data["showRankingScore"]
    
    try:
        result = service.search(uid, query, search_params)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== Settings ====================

@index_bp.route("/<string:uid>/settings", methods=["GET"])
def get_settings(project_id, uid):
    """Get all settings for an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        settings = service.get_settings(uid)
        return jsonify({"success": True, "data": settings})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings", methods=["PATCH"])
def update_settings(project_id, uid):
    """Update settings for an index"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    data = request.get_json()
    
    try:
        result = service.update_settings(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings", methods=["DELETE"])
def reset_settings(project_id, uid):
    """Reset settings to default"""
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    
    try:
        result = service.reset_settings(uid)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Individual settings endpoints
@index_bp.route("/<string:uid>/settings/searchable-attributes", methods=["GET"])
def get_searchable_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        attrs = service.get_searchable_attributes(uid)
        return jsonify({"success": True, "data": attrs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/searchable-attributes", methods=["PUT"])
def update_searchable_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_searchable_attributes(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/displayed-attributes", methods=["GET"])
def get_displayed_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        attrs = service.get_displayed_attributes(uid)
        return jsonify({"success": True, "data": attrs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/displayed-attributes", methods=["PUT"])
def update_displayed_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_displayed_attributes(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/filterable-attributes", methods=["GET"])
def get_filterable_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        attrs = service.get_filterable_attributes(uid)
        return jsonify({"success": True, "data": attrs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/filterable-attributes", methods=["PUT"])
def update_filterable_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_filterable_attributes(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/sortable-attributes", methods=["GET"])
def get_sortable_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        attrs = service.get_sortable_attributes(uid)
        return jsonify({"success": True, "data": attrs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/sortable-attributes", methods=["PUT"])
def update_sortable_attributes(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_sortable_attributes(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/ranking-rules", methods=["GET"])
def get_ranking_rules(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        rules = service.get_ranking_rules(uid)
        return jsonify({"success": True, "data": rules})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/ranking-rules", methods=["PUT"])
def update_ranking_rules(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_ranking_rules(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/synonyms", methods=["GET"])
def get_synonyms(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        synonyms = service.get_synonyms(uid)
        return jsonify({"success": True, "data": synonyms})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/synonyms", methods=["PUT"])
def update_synonyms(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_synonyms(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/stop-words", methods=["GET"])
def get_stop_words(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        stop_words = service.get_stop_words(uid)
        return jsonify({"success": True, "data": stop_words})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/stop-words", methods=["PUT"])
def update_stop_words(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_stop_words(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/typo-tolerance", methods=["GET"])
def get_typo_tolerance(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        typo = service.get_typo_tolerance(uid)
        return jsonify({"success": True, "data": typo})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/typo-tolerance", methods=["PATCH"])
def update_typo_tolerance(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_typo_tolerance(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/pagination", methods=["GET"])
def get_pagination(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        pagination = service.get_pagination(uid)
        return jsonify({"success": True, "data": pagination})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/pagination", methods=["PATCH"])
def update_pagination(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_pagination(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/faceting", methods=["GET"])
def get_faceting(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        faceting = service.get_faceting(uid)
        return jsonify({"success": True, "data": faceting})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/faceting", methods=["PATCH"])
def update_faceting(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_faceting(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/dictionary", methods=["GET"])
def get_dictionary(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        dictionary = service.get_dictionary(uid)
        return jsonify({"success": True, "data": dictionary})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/dictionary", methods=["PUT"])
def update_dictionary(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_dictionary(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/separator-tokens", methods=["GET"])
def get_separator_tokens(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    try:
        tokens = service.get_separator_tokens(uid)
        return jsonify({"success": True, "data": tokens})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@index_bp.route("/<string:uid>/settings/separator-tokens", methods=["PUT"])
def update_separator_tokens(project_id, uid):
    service = get_meilisearch_service(project_id)
    if not service:
        return jsonify({"success": False, "error": "Project not found"}), 404
    data = request.get_json()
    try:
        result = service.update_separator_tokens(uid, data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

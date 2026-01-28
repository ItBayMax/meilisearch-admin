"""
Flask application factory
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, jsonify
from flask_cors import CORS

from backend.utils.config import config
from backend.models import db
from backend.api import project_bp, index_bp, task_bp, key_bp


def setup_logging(app):
    """Setup application logging"""
    log_config = config.logging
    log_level = getattr(logging, log_config.get("level", "INFO").upper())
    log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_dir = Path(log_config.get("output_dir", "./logs"))
    log_file = log_config.get("file_name", "meilisearch_admin.log")
    max_bytes = log_config.get("max_bytes", 10485760)
    backup_count = log_config.get("backup_count", 5)
    
    # Create log directory if not exists
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_file
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Configure app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Configure root logger for libraries
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    
    # Configure werkzeug logger
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(log_level)
    werkzeug_logger.addHandler(file_handler)
    
    app.logger.info(f"Logging initialized - Level: {log_config.get('level', 'INFO')}, Path: {log_path}")


def create_app(config_path: str = None):
    """Create and configure Flask application"""
    
    # Reload config if custom path provided
    if config_path:
        config.load_config(config_path)
    
    app = Flask(__name__)
    
    # Setup logging
    setup_logging(app)
    
    # Configure app
    app.config["SECRET_KEY"] = config.app.get("secret_key", "dev-secret-key")
    app.config["DEBUG"] = config.app.get("debug", False)
    app.config["JSON_AS_ASCII"] = False
    app.config["JSON_SORT_KEYS"] = False
    
    # Configure CORS
    if config.cors.get("enabled", True):
        origins = config.cors.get("origins", ["*"])
        CORS(app, origins=origins, supports_credentials=True)
    
    # Initialize database
    with app.app_context():
        db.create_tables()
    
    # Register blueprints
    app.register_blueprint(project_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(key_bp)
    
    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "version": config.app.get("version", "1.0.0"),
        })
    
    # Root endpoint
    @app.route("/", methods=["GET"])
    def root():
        return jsonify({
            "name": config.app.get("name", "Meilisearch Admin"),
            "version": config.app.get("version", "1.0.0"),
            "api_prefix": "/api",
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "error": "Internal server error"}), 500
    
    # Teardown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.close_session()
    
    return app


# Application instance for WSGI servers
app = create_app()


if __name__ == "__main__":
    host = config.server.get("host", "0.0.0.0")
    port = config.server.get("port", 5000)
    debug = config.app.get("debug", True)
    
    print(f"Starting {config.app.get('name')} on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

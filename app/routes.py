from flask import Blueprint, request, jsonify
from libs.PaperRetrievalService.retriever_manager import RetrieverManager
import logging

# Define a blueprint for modularity
main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/retrieve_papers", methods=["POST"])
def retrieve_papers_api():
    """API to retrieve papers based on the request payload."""
    data = request.get_json()

    # Extract request data
    fields_to_search = data.get("fields_to_search")
    output_dir = data.get("output_dir")
    start_date = data.get("start_date")  # Required: format 'YYYY-MM-DD' or "NOW"
    end_date = data.get("end_date")  # Required: format 'YYYY-MM-DD' or "NOW"

    if not fields_to_search or not output_dir or not start_date or not end_date:
        return (
            jsonify(
                {
                    "error": "fields_to_search, output_dir, start_date, and end_date are required."
                }
            ),
            400,
        )

    try:
        all_papers_metadata = RetrieverManager.retrieve_from_all(
            fields_to_search, output_dir, start_date, end_date
        )
        return (
            jsonify(
                {
                    "message": "Papers retrieved successfully",
                    "papers_metadata": all_papers_metadata,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": "Failed to retrieve papers", "details": str(e)}), 500

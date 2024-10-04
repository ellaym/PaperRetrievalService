import json
import importlib
import logging
from pathlib import Path


class RetrieverManager:
    """Manager to load and retrieve papers from all configured retrievers."""

    retrievers = {}

    @staticmethod
    def load_config(config_path="retrievers_config.json"):
        """Load retrievers from a config file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Retriever config file {config_path} not found.")

        with open(config_path, "r") as file:
            config = json.load(file)

        # Dynamically import and instantiate retrievers
        for _, class_path in config["retrievers"].items():
            module_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            retriever_class = getattr(module, class_name)
            RetrieverManager.retrievers[class_name] = retriever_class()

    @staticmethod
    def retrieve_from_all(
        fields_to_search: str, output_dir: str, start_date: str, end_date: str
    ):
        """Retrieve papers from all configured retrievers and return metadata (files, title, summary, authors)."""
        if not RetrieverManager.retrievers:
            # Load retrievers if not already loaded
            RetrieverManager.load_config()

        all_papers_metadata = (
            []
        )  # This will contain metadata (title, summary, authors, file paths)

        # Iterate through all retrievers and download papers
        for retriever in RetrieverManager.retrievers.values():
            logging.info(f"Retrieving papers from {retriever.__class__.__name__}")
            try:
                papers_metadata = retriever.retrieve_papers(
                    fields_to_search, output_dir, start_date, end_date
                )
                all_papers_metadata.extend(
                    papers_metadata
                )  # Add all metadata (title, authors, summary, file)
            except Exception as e:
                logging.error(
                    f"Failed to retrieve papers from {retriever.__class__.__name__}: {str(e)}"
                )

        return all_papers_metadata

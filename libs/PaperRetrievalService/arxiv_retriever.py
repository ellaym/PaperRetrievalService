import arxiv
import os
import time
import logging
from pathlib import Path
from datetime import datetime
from libs.PaperRetrievalService.base_retriever import (
    PaperRetriever,
)  # Import base class


class ArxivRetriever(PaperRetriever):
    MAX_TITLE_LENGTH = 50
    
    FIELD_TO_QUERY_MAP = {
        "algorithms": "cs.DS",
        "cryptography": "cs.CR"
    }

    def generate_search_query(self, fields_to_search):
        """Generate a search query based on the fields to search."""
        search_query = " OR ".join(
            [self.FIELD_TO_QUERY_MAP[field] for field in fields_to_search]
        )
        return search_query

    def retrieve_papers(
        self, fields_to_search, output_dir, start_date, end_date, delay_seconds=3
    ):
        search_query = self.generate_search_query(fields_to_search)
        
        """Retrieve papers from Arxiv with metadata (title, authors, summary, file path)."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        logging.info(
            f"Starting paper retrieval process from {start_date} to {end_date} with query: {search_query}"
        )

        if start_date == "NOW":
            start_date = str(datetime.now().date())
        if end_date == "NOW":
            end_date = str(datetime.now().date())

        # Ensure date format is correct
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Initialize the Arxiv client
        client = arxiv.Client(page_size=100, delay_seconds=delay_seconds)
        search_query += f" AND submittedDate:[{start_date} TO {end_date}]"
        search = arxiv.Search(
            query=search_query,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        papers_metadata = []  # To store metadata (title, authors, summary, file path)

        index = 0
        
        for result in client.results(search):
            index +=1
            if (index > 5):
                break
            sanitized_title = (
                result.title[: self.MAX_TITLE_LENGTH]
                .replace(" ", "_")
                .replace("/", "_")
            )
            pdf_filename = f"{result.get_short_id()}_{sanitized_title}.pdf"
            pdf_path = Path(output_dir) / pdf_filename

            # Download the paper's PDF
            try:
                result.download_pdf(filename=pdf_path)
                logging.info(f"Downloaded {pdf_filename} to {pdf_path}")
                papers_metadata.append(
                    {
                        "title": result.title,
                        "authors": [author.name for author in result.authors],
                        "summary": result.summary,
                        "file_path": str(pdf_path),
                    }
                )
            except Exception as e:
                logging.error(f"Failed to download paper: {result.title}. Error: {e}")

        return papers_metadata

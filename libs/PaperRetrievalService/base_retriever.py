from abc import ABC, abstractmethod


class PaperRetriever(ABC):
    """Abstract base class for paper retrievers."""

    @abstractmethod
    def retrieve_papers(
        self, fields_to_search, output_dir, start_date, end_date, delay_seconds=3
    ):
        """Method to retrieve papers based on search query and date range."""
        pass

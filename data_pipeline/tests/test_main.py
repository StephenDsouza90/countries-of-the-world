"""
This module contains the tests for the main method of the DataPipelineOrchestrator class.
"""

from unittest.mock import patch, MagicMock

from backend.db.manager import DatabaseManager
from data_pipeline.main import DataPipelineOrchestrator
from data_pipeline.client import RestCountriesAPIClient
from data_pipeline.processor import Processor
from data_pipeline.handler import Handler


def test_data_pipeline_orchestrator_main():
    """
    Test the main method of the DataPipelineOrchestrator class.
    """
    mock_countries = [
        {
            "name": {"common": "Country1"},
            "region": "Region1",
            "population": 1000,
            "area": 10,
        },
        {
            "name": {"common": "Country2"},
            "region": "Region2",
            "population": 1000,
            "area": 10,
        },
    ]

    mock_new_countries = [
        {
            "name": "Country1",
            "region": "Region1",
            "population": 1000,
            "area": 10,
            "population_density": 100,
        }
    ]

    mock_updated_countries = [
        {
            "name": "Country2",
            "population": 2000,
            "area": 20,
            "population_density": 100,
        }
    ]

    mock_db_manager = MagicMock(spec=DatabaseManager)
    mock_cache_manager = MagicMock()

    with (
        patch.object(
            RestCountriesAPIClient, "fetch_countries", return_value=mock_countries
        ) as mock_fetch_countries,
        patch.object(
            Processor,
            "process",
            return_value=(mock_new_countries, mock_updated_countries),
        ) as mock_process,
        patch.object(
            Handler, "add_and_update_countries_to_database"
        ) as mock_add_and_update,
        patch.object(
            Handler, "add_and_update_countries_to_cache"
        ) as mock_add_and_update_cache,
    ):
        orchestrator = DataPipelineOrchestrator(mock_db_manager, mock_cache_manager)
        orchestrator.main()

        mock_fetch_countries.assert_called_once()
        mock_process.assert_called_once_with(
            mock_countries, mock_db_manager, mock_cache_manager
        )
        mock_add_and_update.assert_called_once_with(
            mock_db_manager, mock_new_countries, mock_updated_countries
        )
        mock_add_and_update_cache.assert_called_once_with(
            mock_cache_manager, mock_new_countries, mock_updated_countries
        )

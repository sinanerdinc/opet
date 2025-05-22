import pytest
from click.testing import CliRunner
from opet.main import cli
from opet.exceptions import ProvinceNotFoundError # Ensure this is imported

@pytest.fixture
def mock_opet_client(mocker):
    """Fixture for mocking OpetApiClient."""
    # Mock the class OpetApiClient where it's imported in opet.main
    mock_client_class = mocker.patch('opet.main.OpetApiClient')
    # Create an instance from the mocked class to be returned by the constructor
    mock_client_instance = mock_client_class.return_value
    return mock_client_instance

def test_cli_success(mock_opet_client):
    """Test CLI for successful execution."""
    province_id = "34"
    expected_json_output = """{
  "results": {
    "province": "Istanbul",
    "lastUpdate": "2023-01-01T10:00:00",
    "prices": [
      {
        "name": "Petrol",
        "amount": 20.0
      }
    ]
  }
}"""
    # Configure the 'price' method of the *instance*
    mock_opet_client.price.return_value = expected_json_output

    runner = CliRunner()
    result = runner.invoke(cli, ["--il", province_id])

    assert result.exit_code == 0
    # Strip trailing newline from result.output for accurate comparison
    assert result.output.strip() == expected_json_output.strip()
    # Assert that the 'price' method was called with the province_id as a positional argument
    mock_opet_client.price.assert_called_once_with(province_id)

def test_cli_province_not_found(mock_opet_client):
    """Test CLI when a province is not found."""
    province_id = "00"
    # The error message from api.py: f"Sistemde {province_id} plaka koduna ait bir il bulunamadı."
    # The test instruction says "error message from the exception is printed"
    # Let's use the actual error message the user would see.
    error_message = f"Sistemde {province_id} plaka koduna ait bir il bulunamadı."
    
    # Configure the mock client's price method to raise ProvinceNotFoundError
    mock_opet_client.price.side_effect = ProvinceNotFoundError(error_message)

    runner = CliRunner()
    result = runner.invoke(cli, ["--il", province_id])

    assert result.exit_code == 0  # As per instruction, exception is caught in main.py
    assert error_message in result.output
    # Assert that the 'price' method was called with the province_id as a positional argument
    mock_opet_client.price.assert_called_once_with(province_id)

def test_cli_general_exception(mock_opet_client):
    """Test CLI for handling general exceptions."""
    province_id = "34"
    error_message = "A general error occurred"
    
    # Configure the mock client's price method to raise a generic Exception
    mock_opet_client.price.side_effect = Exception(error_message)

    runner = CliRunner()
    result = runner.invoke(cli, ["--il", province_id])

    # main.py catches Exception and prints it, then exits. Default exit code is 0.
    assert result.exit_code == 0 
    assert error_message in result.output # Check if the generic error message is printed
    # Assert that the 'price' method was called with the province_id as a positional argument
    mock_opet_client.price.assert_called_once_with(province_id)

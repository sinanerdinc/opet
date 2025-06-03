import pytest
from click.testing import CliRunner
from opet.main import cli
from opet.exceptions import ProvinceNotFoundError


@pytest.fixture
def runner():
    """Fixture for Click CLI testing."""
    return CliRunner()


def test_cli_success(runner, mocker):
    """Test successful CLI execution."""
    mock_client = mocker.patch('opet.main.OpetApiClient')
    mock_instance = mock_client.return_value
    mock_instance.price.return_value = '{"results": {"test": "data"}}'

    result = runner.invoke(cli, ['--il', '34'])

    assert result.exit_code == 0
    assert result.output == '{"results": {"test": "data"}}\n'

    mock_client.assert_called_once()
    mock_instance.price.assert_called_once_with('34')


def test_cli_province_not_found(runner, mocker):
    """Test CLI behavior when province is not found."""
    mock_client = mocker.patch('opet.main.OpetApiClient')
    mock_instance = mock_client.return_value
    mock_instance.price.side_effect = ProvinceNotFoundError(
        "Sistemde 99 plaka koduna ait bir il bulunamadı."
    )

    result = runner.invoke(cli, ['--il', '99'])

    assert result.exit_code == 1
    expected_error = "Error: Sistemde 99 plaka koduna ait bir il bulunamadı."
    assert expected_error in result.output


def test_cli_general_exception(runner, mocker):
    """Test CLI behavior when an unexpected error occurs."""
    mock_client = mocker.patch('opet.main.OpetApiClient')
    mock_instance = mock_client.return_value
    mock_instance.price.side_effect = Exception("Unexpected error")

    result = runner.invoke(cli, ['--il', '34'])

    assert result.exit_code == 1
    assert "An unexpected error occurred: Unexpected error" in result.output

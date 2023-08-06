from mock import MagicMock

from ..constants import config_json


def test_deposit_accounts_generator():
    from tap_mambu.tap_mambu_refactor.tap_generators.deposit_accounts_generator import DepositAccountsGenerator
    client_mock = MagicMock()
    client_mock.page_size = int(config_json.get("page_size", 500))
    client_mock.request = MagicMock()
    generator = DepositAccountsGenerator(stream_name="deposit_accounts",
                                            client=client_mock,
                                            config=config_json,
                                            state={'currently_syncing': 'deposit_accounts'},
                                            sub_type="self")
    assert generator.endpoint_path == "deposits:search"
    assert generator.endpoint_bookmark_field == "lastModifiedDate"
    assert generator.endpoint_sorting_criteria == {
            "field": "lastModifiedDate",
            "order": "ASC"
        }
    assert generator.endpoint_filter_criteria == [
            {
                "field": "lastModifiedDate",
                "operator": "AFTER",
                "value": '2021-06-01'
            }
        ]

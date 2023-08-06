import inspect
import os

from mock import MagicMock

from ..constants import config_json
from ..helpers import GeneratorMock

FIXTURES_PATH = f"{os.path.dirname(os.path.abspath(inspect.stack()[0][1]))}/Fixtures"


def test_loan_accounts_processor():
    from singer.catalog import Catalog
    catalog = Catalog.load(f"{FIXTURES_PATH}/processor_catalog.json")
    client_mock = MagicMock()

    from tap_mambu.tap_mambu_refactor.tap_processors.loan_accounts_processor import LoanAccountsProcessor
    processor = LoanAccountsProcessor(catalog=catalog,
                                      stream_name="loan_accounts",
                                      client=client_mock,
                                      config=config_json,
                                      state={'currently_syncing': 'loan_accounts'},
                                      sub_type="self",
                                      generators=[GeneratorMock([])])

    assert processor.endpoint_deduplication_key == "id"
    assert processor.endpoint_child_streams == ["loan_repayments"]
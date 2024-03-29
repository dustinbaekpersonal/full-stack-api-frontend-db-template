"""Test for items.py."""
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "store_name, expected_status, expected_response",
    [
        (
            "Waitrose",
            200,
            [
                {
                    "id": 1,
                    "product_name": "milk",
                    "stock_level": 0,
                    "store_id": 1,
                    "updated_date": "2024-03-03T21:41:00.529000",
                },
            ],
        ),  # successful API call
        (
            "Aldi",
            404,
            {"detail": "Store 'Aldi' not found."},
        ),  # wrong API call
    ],
)
def test_get_stock_levels_by_store_name(
    store_name: str, expected_status: int, expected_response: dict[str, Any]
) -> None:
    """Unit test for get_stock_levels."""
    response = client.get(f"/inventory/{store_name}/")
    assert response.status_code == expected_status
    assert response.json() == expected_response


# # TODO: Ideally we should patch _read_db function
# def test_get_stock_levels_db(monkeypatch: pytest.MonkeyPatch) -> None:
#     """Unit test for get_stock_levels to read from database."""
#     def replace_read_db() -> pd.DataFrame:
#         """Function to replace """
#         return pd.DataFrame(
#             {
#                 "stock_level": ["10"],
#                 "datetime": ["20"],
#             },
#             index = ['milk']
#         )
#     # Use monkeypatch to replace the original function with the mock
#     monkeypatch.setattr("api.items._read_db", replace_read_db)
#     response = client.get("/stock-levels", params={"product":"milk"})
#     assert response.status_code == 200
#     assert response.json() == {
#         "stock_level":'10',
#         "datetime": '20',
#         }

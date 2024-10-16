import json
import pytest
from graphene_django.utils.testing import graphql_query


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


@pytest.mark.django_db
def test_get_ingredients(client_query):
    response = client_query(
        """
        query {
            allIngredients {
                edges {
                    node {
                        name
                        id
                        notes
                    }
                }
            }
        }
        """,
    )

    content = json.loads(response.content)
    print(content)
    assert "errors" not in content
    assert len(content["data"]["allIngredients"]["edges"]) == 4


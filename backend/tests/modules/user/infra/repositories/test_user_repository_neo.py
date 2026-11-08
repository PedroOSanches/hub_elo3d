from uuid import uuid7

import pytest
from src.modules.user.domain.entities.address import Address
from src.modules.user.domain.entities.user import User
from src.modules.user.infra.repositories.user_repository_neoj import UserRepositoyNeoJ
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory

@pytest.fixture
def get_connection():
    return Neo4JConnectionFactory()

class Test_UserRepositoryNeoJ:

    @pytest.skip('Needs Neo4J')
    def test_create_user(self, get_connection):

        repo = UserRepositoyNeoJ(connection=get_connection)
        user_id = uuid7()
        user = User(
            user_id=user_id,
            name='Angela',
            email='angela@aacd.com',
            address=Address(
                street='Praça Teste',
                number='3280',
                neighborhood='Vila Teste',
                city='São Caetano do Sul',
                state='SP',
                cep='000000000',
                address_details='Apto. 12'
            ),
            phone='+5511999999999',
            role='user_hospital'
        )
        created_user = repo.create_user(user=user)

        assert created_user.user_id == user_id
        assert created_user.name == 'Angela'
from uuid import UUID, uuid7

import pytest
from src.modules.user.domain.entities.address import Address
from src.modules.user.domain.entities.user import User
from src.modules.user.infra.repositories.user_repository_neoj import UserRepositoyNeoJ, DuplicatedUser, NoUsersFound
from src.shared.environments.neo4j_connection_factory import Neo4JConnectionFactory
from src.shared.utils.password_hasher import gerar_hash_senha
def get_connection():
    return Neo4JConnectionFactory()

@pytest.fixture
def user():
    return User(
            user_id='01a1bbf0-5fff-7615-8970-41c994a6e31f',
            name='Angela',
            email='angela@example.com',
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
            role='user_hospital',
            password_hash=gerar_hash_senha('!Teste123')
        )

class Test_UserRepositoryNeoJ:
    @pytest.mark.skip('Needs Neo4J')
    def test_create_user(self, user):

        repo = UserRepositoyNeoJ(connection=get_connection())
        created_user = repo.create_user(user=user)

        print(created_user.user_id)
        assert created_user.user_id == user.user_id
        assert created_user.name == 'Angela'
    
    @pytest.mark.skip('Needs Neo4J')
    def test_create_user_duplicated(self, user):

        with pytest.raises(DuplicatedUser):
            repo = UserRepositoyNeoJ(connection=get_connection())
            repo.create_user(user=user)
    
    @pytest.mark.skip('Needs Neo4J')
    def test_get_user(self, user):

        repo = UserRepositoyNeoJ(connection=get_connection())
        user_stored = repo.get_user(user_id=user.user_id)

        assert user_stored.user_id == user.user_id
        assert user_stored.name == user.name
        assert user_stored.user_id is not None 
    
    @pytest.mark.skip('Needs Neo4J')
    def test_get_user_no_users_found(self, user):
        with pytest.raises(NoUsersFound):
            repo = UserRepositoyNeoJ(connection=get_connection())
            user_stored = repo.get_user(user_id=UUID('01a1bc0c-e700-7522-92dd-e54d15712d3b'))
    
    @pytest.mark.skip('Needs Neo4J')
    def test_get_user_all(self):
        repo = UserRepositoyNeoJ(connection=get_connection())
        users = repo.get_all_users()

        assert str(users[0].user_id) == '01a1bbf0-5fff-7615-8970-41c994a6e31f'
        assert str(users[0].name) == 'Angela'
    
    @pytest.mark.skip('Needs Neo4J')
    def test_get_user_by_email(self, user):
        repo = UserRepositoyNeoJ(connection=get_connection())

        user_stored = repo.get_user_by_email(user.email)

        assert user_stored.user_id == user.user_id
        assert user_stored.role == user.role

    @pytest.mark.skip('Needs Neo4J')
    def test_get_user_by_email_no_user_found(self, user):
        with pytest.raises(NoUsersFound):
            repo = UserRepositoyNeoJ(connection=get_connection())
            user_stored = repo.get_user_by_email('no_user@example.com')

    @pytest.mark.skip('Needs Neo4J')
    def test_update(self, user):
        repo = UserRepositoyNeoJ(connection=get_connection())

        user = User(
            user_id=user.user_id,
            name='Angela',
            email='angela@maua.br',
            address=Address(
                street='Praça Teste',
                number='3280',
                neighborhood='Vila Teste',
                city='São Caetano do Sul',
                state='SP',
                cep='000000000',
                address_details='Apto. 12'
            ),
            phone='+5511967876564',
            role='user_hospital'
            )
        
        updated_user = repo.update_user(user)

        assert updated_user.user_id == user.user_id
        assert updated_user.phone == user.phone
        assert updated_user.email == user.email

    @pytest.mark.skip('Needs Neo4J')
    def test_update_no_user_found(self, user):
        
        repo = UserRepositoyNeoJ(connection=get_connection())
        user = User(
            user_id=UUID('01a1bc0c-e700-7522-92dd-e54d15712d3b'),
            name='Angela',
            email='angela@maua.br',
            address=Address(
                street='Praça Teste',
                number='3280',
                neighborhood='Vila Teste',
                city='São Caetano do Sul',
                state='SP',
                cep='000000000',
                address_details='Apto. 12'
            ),
            phone='+5511967876564',
            role='user_hospital'
            )
        
        with pytest.raises(NoUsersFound):
            updated_user = repo.update_user(user)

    @pytest.mark.skip('Needs Neo4J')
    def test_delete(self, user):
        repo = UserRepositoyNeoJ(get_connection())

        user_deleted = repo.delete_user(user.user_id)

        assert user_deleted.user_id == user.user_id
        assert user_deleted.name == user.name
        assert user_deleted.email == 'angela@maua.br'
    
    @pytest.mark.skip('Needs Neo4J')
    def test_delete_no_found_user(self, user):
        repo = UserRepositoyNeoJ(get_connection())

        with pytest.raises(NoUsersFound):
            user_deleted = repo.delete_user(UUID('01a1bc0c-e700-7522-92dd-e54d15712d3b'))
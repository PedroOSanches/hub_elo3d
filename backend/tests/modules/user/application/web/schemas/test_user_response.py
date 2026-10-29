import pydantic

from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema
from src.modules.user.domain.entities.endereco import Address


class Test_CreateUserResponse:

    def test_create_user_response(self):
        UserResponseSchema(
            id='1e82ade2-961f-472d-9f32-b86647c63616',
            name="Teste",
            email="teste@example.com",
            phone="+5511999990000",
            address=Address(
                logradouro="Teste",
                numero="000",
                bairro="Praça do Teste",
                cidade="Testenópolis",
                estado="TO",
                cep="00000-000"
            ),
            institution_id='02271956-3d88-45a5-a511-d943ef9ddeb6',
            role="hospital"
        )
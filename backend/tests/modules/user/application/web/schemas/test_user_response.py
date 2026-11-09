import pydantic

from src.modules.user.application.web.schemas.user_response_schema import UserResponseSchema
from src.modules.user.domain.entities.address import Address


class Test_CreateUserResponse:

    def test_create_user_response(self):
        UserResponseSchema(
            user_id='1e82ade2-961f-472d-9f32-b86647c63616',
            name="Teste",
            email="teste@example.com",
            phone="+5511999990000",
            address=Address(
                street="Teste",
                number="000",
                neighborhood="Praça do Teste",
                city="Testenópolis",
                state="TO",
                cep="00000-000"
            ),
            role="hospital"
        )
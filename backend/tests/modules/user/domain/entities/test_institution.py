from src.modules.user.domain.entities.institution import Institution, EntitieError



class Test_Institution:

    def test_institution(self):
        Institution(
            name="Teste teste",
        )
        
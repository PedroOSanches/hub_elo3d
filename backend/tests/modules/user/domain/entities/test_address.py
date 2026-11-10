import pytest
from src.modules.user.domain.entities.address import Address, EntitieError


class Test_Address:

    def test_address(self):
        address = Address(
            street="Teste",
            number="45",
            neighborhood="Santo Teste",
            city="Teste",
            state="SP",
            cep="00000-000",
            address_details="Apto. Teste"
        )

    def test_logragrouro_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        street="T",
                        number="45",
                        city="Teste",
                        neighborhood="Santo Teste",
                        state="SP",
                        cep="00000-000",
                        address_details="Apto. Teste"
                    )

    def test_number_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        street="T",
                        number=4,
                        neighborhood="Santo Teste",
                        city="Teste",
                        state="SP",
                        cep="00000-000",
                        address_details="Apto. Teste"
                    )
            
    def test_neighborhood_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        street="T",
                        number="345",
                        city="Teste",
                        neighborhood="S",
                        state="SP",
                        cep="00000-000",
                        address_details="Apto. Teste"
                    )


    def test_city_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        street="T",
                        number="345",
                        neighborhood="Sé",
                        city="Teste",
                        state="São Paulo",
                        cep="00000-000",
                        address_details="Apto. Teste"
                    )
    
    def test_cep_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        street="T",
                        number="345",
                        neighborhood="Sé",
                        city="Teste",
                        state="SP",
                        cep="00000000",
                        address_details="Apto. Teste"
                    )

    def test_address_details_invalid_type(self):
        with pytest.raises(EntitieError):
            address = Address(
                        street="T",
                        number="345",
                        neighborhood="Sé",
                        city="Teste",
                        state="São Paulo",
                        cep="00000000",
                        address_details=13
                    )
import pytest
from src.modules.user.domain.entities.endereco import Address, EntitieError


class Test_Address:

    def test_address(self):
        address = Address(
            logradouro="Teste",
            numero="45",
            bairro="Santo Teste",
            cidade="Teste",
            estado="SP",
            cep="00000-000",
            complemento="Apto. Teste"
        )

    def test_logragrouro_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        logradouro="T",
                        numero="45",
                        cidade="Teste",
                        bairro="Santo Teste",
                        estado="SP",
                        cep="00000-000",
                        complemento="Apto. Teste"
                    )

    def test_numero_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        logradouro="T",
                        numero=4,
                        bairro="Santo Teste",
                        cidade="Teste",
                        estado="SP",
                        cep="00000-000",
                        complemento="Apto. Teste"
                    )
            
    def test_bairro_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        logradouro="T",
                        numero="345",
                        cidade="Teste",
                        bairro="S",
                        estado="SP",
                        cep="00000-000",
                        complemento="Apto. Teste"
                    )


    def test_cidade_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        logradouro="T",
                        numero="345",
                        bairro="Sé",
                        cidade="Teste",
                        estado="São Paulo",
                        cep="00000-000",
                        complemento="Apto. Teste"
                    )
    
    def test_cep_invalid(self):
        with pytest.raises(EntitieError):
            address = Address(
                        logradouro="T",
                        numero="345",
                        bairro="Sé",
                        cidade="Teste",
                        estado="SP",
                        cep="00000000",
                        complemento="Apto. Teste"
                    )

    def test_complemento_invalid_type(self):
        with pytest.raises(EntitieError):
            address = Address(
                        logradouro="T",
                        numero="345",
                        bairro="Sé",
                        cidade="Teste",
                        estado="São Paulo",
                        cep="00000000",
                        complemento=13
                    )
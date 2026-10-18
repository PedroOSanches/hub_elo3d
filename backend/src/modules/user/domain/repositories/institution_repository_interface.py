import abc
from abc import abstractmethod


from src.modules.user.domain.entities.institution import Institution

class IInstitutionRepository(abc.ABC):
    @abstractmethod
    def get_institution(self, id: str) -> Institution:
        """
        Retorna um objeto "Institution" a partir do seu ID

        Em caso não encontrado retorna NoInstitutionFound
        """

        pass

    @abstractmethod
    def get_all_institutions(self) -> list[Institution]:
        """
        Retorna todos os usuários


        Em caso de nenhum usuário encontrado retorna NoInstitutionFound
        """
        pass

    @abstractmethod
    def create_institution(self, institution: Institution) -> Institution:
        """
        Cria um novo usuário

        Em caso de sucesso retorna o usuario criado

        Caso encontre um usuário já existente com as mesmas credencias retorna DuplicatedInstitution
        """
        pass

    @abstractmethod
    def update_institution(
            self, 
            id: str, 
            updated_institution: Institution
            ) -> Institution:
        """
        Atualiza os campos de um usuário de acordo com o id

        Retorna o usuário com os campos atualizados


        Em caso de haver mais de um usuário registrado retorna DuplicatedUser
        Em caso de não encontre nenhum usuario retorna NoInstitutionFound
        """

        pass
    
    @abstractmethod
    def delete_institution(self, id: str) -> Institution:
        """
        Deleta um usuário retorna o Institution deletado

        Caso o ID não for encontrado retorna NoInstitutionFound
        """
        pass

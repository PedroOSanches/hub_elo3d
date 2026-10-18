from uuid import UUID

from src.modules.user.domain.entities.institution import Institution
from src.modules.user.domain.repositories.institution_repository_interface import IInstitutionRepository
from src.modules.user.domain.errors.institution_usecase_errors import DuplicatedInstitution, NoInstitutionFound

class InstitutionRepositoryMock(IInstitutionRepository):
    def __init__(self):
        self.institutions = [
            Institution(
                id = UUID("f65e238b-f673-499d-b48c-e65e9b8dfa82"),
                name="Instituto teste de Tecnologia",
            ),
            Institution(
                id = UUID("7ed02789-516b-4a03-99b9-cbebaca72686"),
                name="Hospital teste",
            ),
        ]

    def get_institution(self, id: str) -> Institution:
        for institution in self.institutions:
            if str(institution.id) == id:
                return institution

        raise NoInstitutionFound(f"{id}")

    def get_all_institutions(self) -> list[Institution]:
        return self.institutions

    def create_institution(self, institution: Institution) -> Institution:
        for stored_institution in self.institutions:
            if institution.name == stored_institution.name:
                raise DuplicatedInstitution()
        
        self.institutions.append(institution)

        return institution
    
    def update_institution(self,  updated_institution: Institution) -> Institution:
        for i, institution in enumerate(self.institutions):
            if updated_institution.id == institution.id:
                self.institutions[i] = updated_institution
                return self.institutions[i]

        raise NoInstitutionFound(f'{id}')

    def delete_institution(self, id: str) -> Institution:
        for i, institution in enumerate(self.institutions):
            if id == str(institution.id):
                return self.institutions.pop(i)

        raise NoInstitutionFound(f"{id}")

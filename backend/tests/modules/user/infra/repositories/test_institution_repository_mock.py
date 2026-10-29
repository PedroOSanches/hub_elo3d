import pytest

from uuid import UUID
from src.modules.user.infra.repositories.institution_repository_mock import (
    Institution, 
    InstitutionRepositoryMock, 
    NoInstitutionFound, 
    DuplicatedInstitution
    )

class Test_InstitutionRepositoryMock:

    def test_(self):
        repo = InstitutionRepositoryMock()
        institutions = repo.institutions
        institution = Institution(
            id="0334c795-5e71-4c1e-8a0e-ab21a4fcdecf",
            name = "Teste ABC",
        )

        repo.create_institution(institution=institution)

        assert institutions[-1] == institution
        assert institutions[-1].id == UUID('0334c795-5e71-4c1e-8a0e-ab21a4fcdecf')

    def test_get_institution(self):
        repo = InstitutionRepositoryMock()

        institutions = repo.institutions

        institution = repo.get_institution("f65e238b-f673-499d-b48c-e65e9b8dfa82")

        assert institutions[0] == institution
    
    def test_get_all_institution(self):
        repo = InstitutionRepositoryMock()

        institutions = repo.institutions

        get_all_institution = repo.get_all_institutions()

        assert institutions == get_all_institution

    def test_delete_institution(self):
        repo = InstitutionRepositoryMock()

        institution = repo.get_all_institutions()[0]

        deleted_institution = repo.delete_institution("f65e238b-f673-499d-b48c-e65e9b8dfa82")

        assert institution == deleted_institution

    def test_update_institution(self):
        repo = InstitutionRepositoryMock()
        institution = Institution(
            id="f65e238b-f673-499d-b48c-e65e9b8dfa82",
            name = "UTeste",
            )

        repo_institutions = repo.institutions

        institution = repo.update_institution(updated_institution=institution)

        assert institution == repo_institutions[0]

    def test_notfound_get_institution(self):
        repo = InstitutionRepositoryMock()

        with pytest.raises(NoInstitutionFound):
            repo.get_institution("0334c795-5e71-4c1e-8a0e-ab21a4fcdecf")

    def test_notfound_update_institution(self):
            repo = InstitutionRepositoryMock()
    
            with pytest.raises(NoInstitutionFound):
                repo.update_institution(
                    Institution(
                        id="0334c795-5e71-4c1e-8a0e-ab21a4fcdecf",
                        name = "Teste",
                        )
                )

    def test_notfound_delete_institution(self):
        repo = InstitutionRepositoryMock()
    
        with pytest.raises(NoInstitutionFound):
            repo.delete_institution('0334c795-5e71-4c1e-8a0e-ab21a4fcdecf')

    def test_duplicated_institution(self):
        repo = InstitutionRepositoryMock()

        with pytest.raises(DuplicatedInstitution):
            repo.create_institution(
                Institution(
                    name = "Instituto teste de Tecnologia",
                )
    
            )
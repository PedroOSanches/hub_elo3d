from abc import ABC, abstractmethod


class IGatewayStorage(ABC):

    @abstractmethod
    def verify_uploads(
        self,
        file_object_key: str
    ) -> bool:
        """
        Verifica se todos os arquivos associados ao upload_id
        foram enviados corretamente para o armazenamento.

        Raises:
            FileNotFound: Caso algum arquivo não seja encontrado.
        """
        raise NotImplementedError
from abc import ABC, abstractmethod


class IGatewayStorage(ABC):

    @abstractmethod
    def verify_upload(
        self,
        file_object_key: str,
        file_name: str
    ) -> bool:
        """
        Verifica se o arquivos associado ao object_key
        foram enviados corretamente para o armazenamento.

        Raises:
            FileNotFound: Caso algum arquivo não seja encontrado.
        """
        raise NotImplementedError
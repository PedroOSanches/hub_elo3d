from abc import ABC, abstractmethod


class IGatewayStorage(ABC):


    @abstractmethod
    def generate_upload_url(
        self,
        object_key: str,
        content_type: str,
        ) -> str:
        """
        Gera a URL pré-assinada de upload 
        """

        pass
    @abstractmethod
    def generate_download_url(
        self,
        object_key: str,
        file_name: str
        ) -> str:

        """
        Gera URL pré-assinada de download
        """

        pass
        
    @abstractmethod
    def verify_upload(
        self,
        object_keys: list[str]
        ) -> bool:
        """
        Verifica se todos os uploads foram realizados com sucesso
        - True em caso de sucesso
        - False caso ocorra alguma falha
        """
        
        pass
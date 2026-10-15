import bcrypt

def gerar_hash_senha(senha: str):
    senha_bytes = senha.encode('utf-8')

    salt = bcrypt.gensalt()

    hash_senha = bcrypt.hashpw(senha_bytes, salt)

    return hash_senha.decode('utf-8')


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(
        senha.encode('utf-8'),
        senha_hash.encode('utf-8'),
    )
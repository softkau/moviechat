from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings

# Chroma DB는 LLM 검색을 할 때 캐시와 같은 역할을 합니다.
# TMDB, Wikipedia에서 가져온 Movie 정보가 vector 형태로 저장됩니다.
_cached_chroma = None
_cached_embedding = None
_cached_db_path = None

def _init_chroma():
    return Chroma(
        persist_directory=_cached_db_path,
        embedding_function=_cached_embedding
    )

def init_chroma(db_path: str, embedding_function: Embeddings):
    """
    chroma db가 설정되지 않았다면, chroma db를 설정합니다  
    db_path, embedding_function은 다음 init 전까지 계속 유지됩니다
    Args:
        db_path:
            chroma db가 저장될 경로
        embedding_function:
            embedding에 사용할 function
    Returns:
        None
    """
    global _cached_embedding
    global _cached_db_path
    global _cached_chroma

    _cached_embedding = embedding_function
    _cached_db_path = db_path
    _cached_chroma = _init_chroma()


def get_chroma():
    """
    chroma db를 가져옵니다
    Returns:
        ``Chroma`` 객체를 반환합니다.  
        먼저 ``init_chroma()``를 호출하세요
    """
    global _cached_chroma
    if _cached_chroma is None:
        if _cached_db_path and _cached_embedding:
            _cached_chroma = _init_chroma()
        else:
            raise RuntimeError("chroma: use before init_chroma()")

    return _cached_chroma

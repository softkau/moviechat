import os
import wikipedia # type: ignore
import tmdbsimple as tmdb #type: ignore
from common.env import *

# 최신 LangChain 모듈
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.memory import ConversationSummaryBufferMemory

import chroma
CHROMA_DB_PATH = f"{ENV_PROJECT_ROOT}/backend/langchain_modules/chroma_temp"

# API 키 불러오기
# load_dotenv()
tmdb.API_KEY = ENV_TMDB_API_KEY

if not tmdb.API_KEY or not ENV_OPENAI_API_KEY:
    raise ValueError("API 키가 없습니다.")

# LLM 구성
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
embedding = OpenAIEmbeddings()

# Chroma DB 세팅
chroma.init_chroma(CHROMA_DB_PATH, embedding)

# 영화 제목 추출용 프롬프트
title_extract_prompt = PromptTemplate.from_template("""
다음 문장에서 영화 제목이나 등장인물 이름만 출력하세요. 다른 말은 하지 마세요.

문장: {user_input}
영화 제목:
""")

title_chain= title_extract_prompt | llm 

def extract_title_with_llm(user_input: str) -> str:
    response = title_chain.invoke({"user_input": user_input})
    return response.content.strip().strip('"')

# TMDB + Wikipedia
def get_tmdb_overview(title):
    search = tmdb.Search().movie(query=title)
    if not search['results']:
        return ""
    return tmdb.Movies(search['results'][0]['id']).info().get('overview', '')

def get_wikipedia_content(title, lang="ko"):
    wikipedia.set_lang(lang)
    try:
        return wikipedia.page(title).content
    except:
        return ""

def load_data(movie_name):
    db = chroma.get_chroma()
    try:
        existing_titles = {doc.metadata['title'] for doc in db.similarity_search("영화", k=50)}
    except:
        existing_titles = set()

    if movie_name in existing_titles:
        print(f"[스킵됨] '{movie_name}'은 이미 Chroma에 저장되어 있습니다.")
        return

    print(f"[저장됨] '{movie_name}'에 대해 새로 검색합니다.")

    overview = get_tmdb_overview(movie_name)
    wiki = get_wikipedia_content(movie_name) or get_wikipedia_content(movie_name + " (영화)")

    combined = f"[영화 제목] {movie_name}\n\n[TMDB 줄거리]\n{overview}\n\n[Wikipedia 문서]\n{wiki}"
    docs = [Document(page_content=combined, metadata={"title": movie_name})]

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    db.add_documents(split_docs)

# Summarizing Memory 구성
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000,
    return_messages=True
)

def get_qa_chain():
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=chroma.get_chroma().as_retriever(),
        memory=memory,
        return_source_documents=False
    )

while True:
    user_input = input("\n 질문을 입력하세요 (종료하려면 'exit'): ")
    if user_input.lower() == "exit":
        break

    movie_name = extract_title_with_llm(user_input)
    load_data(movie_name)

    qa_chain = get_qa_chain()  # 최신 DB 반영
    result = qa_chain.invoke({"query": user_input})
    print("\n[답변]", result["result"])
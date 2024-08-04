from typing import List
from langchain_community.document_loaders import GitLoader
from dotenv import load_dotenv
from langchain_core.documents import Document

from functions.analyzer.llm import get_llm
from functions.analyzer.parser import RepoResult, repo_result_parser
from functions.analyzer.pricing import correct_instance_price
from functions.analyzer.prompt import repo_analyze_prompt


load_dotenv()
repo_dir = "repo"

filter_doc_name = ["package-lock.json", "node-modules", "poetry.lock", ".DS_Store"]


def load_repo_code(repo_path: str, directory: str = "") -> List[Document]:
    """
    Get all codes from given github repository
    Arguments:
        clone_url (str): Github repository clone url
        branch (str, optional): Branch of github repository to analyze. Default: main
        directory (Str, optional): Specify directory to analyze
    Returns:
        List of langchain Document. One Document corresponds to one file
    """
    loader = GitLoader(
        repo_path=repo_path,
    )
    docs = loader.load()
    if directory != "":
        docs = list(
            filter(lambda d: d.metadata["source"].startswith(f"{directory}/"), docs)
        )
    docs = list(
        filter(
            lambda d: all([f not in d.metadata["source"] for f in filter_doc_name]),
            docs,
        )
    )
    return docs


def analyze_repo(repo_path: str, directory: str = "") -> RepoResult:
    """
    Analyze given github repository and estimate maintenance price, power consumption, and
    carbon footprint

    Arguments:
        clone_url (str): Github repository clone url
        branch (str, optional): Branch of github repository to analyze. Default: main
        directory (Str, optional): Specify directory to analyze

    Returns:
        RepoResult: Analysis results for a given repository
    """
    docs = load_repo_code(repo_path, directory)
    chain = repo_analyze_prompt | get_llm(temperature=0.5) | repo_result_parser
    repo_result = chain.invoke({"GITHUB": docs})
    repo_result: RepoResult = chain.invoke({"GITHUB": docs})
    repo_result.aws = correct_instance_price(repo_result.aws)
    repo_result.gcp = correct_instance_price(repo_result.gcp)
    return repo_result

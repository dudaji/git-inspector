from typing import List
from langchain_community.document_loaders import GitLoader
from dotenv import load_dotenv
from langchain_core.documents import Document

from functions.analyzer.llm import get_llm
from functions.analyzer.parser import RepoResult, repo_result_parser
from functions.analyzer.prompt import repo_analyze_prompt


load_dotenv()
repo_dir = "repo"

filter_doc_name = ["package-lock.json", "node-modules", "poetry.lock", ".DS_Store"]


def load_repo_code(
    clone_url: str, branch: str = "main", folder: str = ""
) -> List[Document]:
    """
    Get all codes from given github repository
    Arguments:
        clone_url (str): Github repository clone url
        branch (str, optional): Branch of github repository to analyze. Default: main
        folder (Str, optional): Specify folder to analyze
    Returns:
        List of langchain Document. One Document corresponds to one file
    """
    project_name = clone_url.split("/")[-1].split(".")[0]
    repo_path = f"{repo_dir}/{project_name}"
    loader = GitLoader(
        clone_url=clone_url,
        repo_path=repo_path,
        branch=branch,
    )
    docs = loader.load()
    if folder != "":
        docs = list(
            filter(lambda d: d.metadata["source"].startswith(f"{folder}/"), docs)
        )
    docs = list(
        filter(
            lambda d: all([f not in d.metadata["source"] for f in filter_doc_name]),
            docs,
        )
    )
    return docs


def analyze_repo(clone_url: str, branch: str = "main", folder: str = "") -> RepoResult:
    """
    Analyze given github repository and estimate maintenance price, power consumption, and
    carbon footprint

    Arguments:
        clone_url (str): Github repository clone url
        branch (str, optional): Branch of github repository to analyze. Default: main
        folder (Str, optional): Specify folder to analyze

    Returns:
        RepoResult: Analysis results for a given repository
    """
    docs = load_repo_code(clone_url, branch, folder)
    chain = repo_analyze_prompt | get_llm(temperature=0.5) | repo_result_parser
    return chain.invoke({"GITHUB": docs})

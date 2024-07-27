from typing import List
from langchain_community.document_loaders import GitLoader
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.runnables import Runnable

from functions.analyzer.prompt import prompt
from functions.analyzer.parser import output_parser


load_dotenv()
repo_dir = "repo"

filter_doc_name = [
    "package-lock.json",
    "node-modules",
    "poetry.lock",
]


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
    loader = GitLoader(
        clone_url=clone_url,
        repo_path=f"{repo_dir}/{project_name}",
        branch=branch,
        # file_filter=lambda file_path: all(
        #     [f not in file_path for f in filter_doc_name]
        # ),
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


def get_chain() -> Runnable:
    """
    Get chain for analyzing
    Returns:
        Runnable Chain of Langchain with prompt and json output parser
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest")
    return prompt | llm | output_parser


def analyze_repo(clone_url: str, branch: str = "main", folder: str = ""):
    """
    Analyze given github repository and estimate maintenance price, power consumption, and
    carbon footprint

    Arguments:
        clone_url (str): Github repository clone url
        branch (str, optional): Branch of github repository to analyze. Default: main
        folder (Str, optional): Specify folder to analyze

    Returns:
        Result of estimation by gemini.
        Refer to Result class in functions/analyzer/parser.py for data structure
    """
    docs = load_repo_code(clone_url, branch, folder)
    chain = get_chain()
    # return chain.invoke({"GITHUB": docs})
    return {"cost": "$1", "power": "super power", "carbon": "1kg"}

from typing import List
from langchain_community.document_loaders import GitLoader
from dotenv import load_dotenv
from langchain_core.documents import Document

from functions.analyzer.llm import get_llm
from functions.analyzer.parser import Instance, RepoResult, repo_result_parser
from functions.analyzer.pricing import correct_instance_price, get_cheapest_instance
from functions.analyzer.prompt import repo_analyze_prompt


load_dotenv()
repo_dir = "repo"

filter_doc_name = ["package-lock.json", "node-modules", "poetry.lock", ".DS_Store"]


def load_repo_code(
    repo_path: str, branch: str = "main", directory: str = ""
) -> List[Document]:
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
        branch=branch,
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


def analyze_repo(repo_path: str, branch: str = "", directory: str = "") -> RepoResult:
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
    docs = load_repo_code(repo_path, branch, directory)
    chain = repo_analyze_prompt | get_llm(temperature=0.5) | repo_result_parser
    repo_result = chain.invoke({"GITHUB": docs})
    repo_result: RepoResult = chain.invoke({"GITHUB": docs})
    repo_result.aws = get_cheapest_instance(correct_instance_price(repo_result.aws))
    repo_result.gcp = get_cheapest_instance(correct_instance_price(repo_result.gcp))
    return repo_result


def analyze_repo_mock(repo_path: str, directory: str = "") -> RepoResult:
    return RepoResult(
        gcp=Instance(
            cloud_provider="GCP",
            name="e2-medium",
            cpu=2,
            ram=4.0,
            storage=10,
            gpu="None",
            region="us-central1",
            cost_per_hour=0.0516,
            description="This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, an e2-medium instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The us-central1 region offers a good balance of cost and latency for many users.",
        ),
        aws=Instance(
            cloud_provider="AWS",
            name="t3.medium",
            cpu=2,
            ram=4.0,
            storage=10,
            gpu="None",
            region="us-east-1",
            cost_per_hour=0.0468,
            description="This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, a t3.medium instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The us-east-1 region offers a good balance of cost and latency for many users.",
        ),
        azure=Instance(
            cloud_provider="Azure",
            name="Standard_B2s",
            cpu=2,
            ram=4.0,
            storage=10,
            gpu="None",
            region="eastus",
            cost_per_hour=0.0456,
            description="This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, a Standard_B2s instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The eastus region offers a good balance of cost and latency for many users.",
        ),
        language_ratio={
            "Kotlin": 1754,
            "Properties": 1056,
            "YAML": 810,
            "Shell": 3607,
            "Batch": 2830,
            "JSON": 2742,
        },
    )

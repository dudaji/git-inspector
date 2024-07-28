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
    return {
        "gcp": {
            "instance": {
                "name": "n1-standard-1",
                "cpu": "1 vCPU",
                "memory": "3.75 GiB",
                "storage": "100 GiB",
                "gpu": "None",
            },
            "pricing": {"monthly": "$14.88", "hourly": "$0.0104"},
            "power_consumption": {"monthly": "216 kWh", "hourly": "1.5 kWh"},
            "carbon_footprint": {"monthly": "17.3 kg CO2", "hourly": "1.2 kg CO2"},
            "description": "GCP's n1-standard-1 instance is chosen for its balance of processing power and cost-effectiveness. The instance provides 1 vCPU and 3.75 GiB of memory, suitable for running the Kotlin Spring Boot application. The instance also includes 100 GiB of persistent disk for storing data and logs. The monthly cost is calculated based on the on-demand pricing of the instance, and the power consumption is estimated based on the instance's specifications. The carbon footprint is calculated based on the power consumption and the average carbon intensity of the GCP data centers.",
        },
        "aws": {
            "instance": {
                "name": "t3.micro",
                "cpu": "1 vCPU",
                "memory": "1 GiB",
                "storage": "100 GiB",
                "gpu": "None",
            },
            "pricing": {"monthly": "$7.20", "hourly": "$0.005"},
            "power_consumption": {"monthly": "168 kWh", "hourly": "1.2 kWh"},
            "carbon_footprint": {"monthly": "13.4 kg CO2", "hourly": "0.9 kg CO2"},
            "description": "AWS's t3.micro instance is selected due to its low cost and sufficient resources for the application. It provides 1 vCPU and 1 GiB of memory, which is enough for the Kotlin Spring Boot application. The instance also has 100 GiB of EBS storage for data and logs. The monthly cost is estimated based on the on-demand pricing of the instance, while the power consumption is calculated based on the instance's specifications. The carbon footprint is calculated based on the power consumption and the average carbon intensity of the AWS data centers.",
        },
        "azure": {
            "instance": {
                "name": "Standard_B1s",
                "cpu": "1 vCPU",
                "memory": "1 GiB",
                "storage": "100 GiB",
                "gpu": "None",
            },
            "pricing": {"monthly": "$5.90", "hourly": "$0.0041"},
            "power_consumption": {"monthly": "144 kWh", "hourly": "1 kWh"},
            "carbon_footprint": {"monthly": "11.5 kg CO2", "hourly": "0.8 kg CO2"},
            "description": "Azure's Standard_B1s instance is chosen due to its cost-effective nature and sufficient resources for the application. It provides 1 vCPU and 1 GiB of memory, which is enough for the Kotlin Spring Boot application. The instance also includes 100 GiB of standard SSD storage for data and logs. The monthly cost is calculated based on the on-demand pricing of the instance, and the power consumption is estimated based on the instance's specifications. The carbon footprint is calculated based on the power consumption and the average carbon intensity of the Azure data centers.",
        },
        "conclusion": {
            "instance": {
                "name": "Standard_B1s",
                "cpu": "1 vCPU",
                "memory": "1 GiB",
                "storage": "100 GiB",
                "gpu": "None",
            },
            "pricing": {"monthly": "$5.90", "hourly": "$0.0041"},
            "power_consumption": {"monthly": "144 kWh", "hourly": "1 kWh"},
            "carbon_footprint": {"monthly": "11.5 kg CO2", "hourly": "0.8 kg CO2"},
            "description": "Based on the analysis, Microsoft Azure's Standard_B1s instance is the most appropriate choice for running the Kotlin Spring Boot application. It offers the lowest monthly cost compared to GCP and AWS, while providing sufficient resources for the application. The instance also has a relatively lower carbon footprint compared to the other two platforms, making it an environmentally responsible option.",
        },
    }

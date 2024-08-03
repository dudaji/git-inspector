from functions.analyzer.parser import (
    repo_result_parser,
    calculate_result_parser,
    best_instance_parser,
)
from langchain.prompts import PromptTemplate

repo_analyze_prompt = PromptTemplate(
    template="""
As an expert in analyzing software repositories and estimating resource consumption and environmental impact, your task is to provide a comprehensive analysis of a GitHub repository.

Instructions
Analyze the structure of the files in the provided GitHub repository by examining the metadata in the documentation.
Identify the entry point of the repository.
Determine the minimum resources required to run the repository on GCP, AWS, and Azure platforms.
Estimate the power consumption, and carbon footprint on each platform.
{format_instruction}
Context
The goal is to gain a detailed understanding of the repository’s requirements and its environmental impact. Your analysis should be thorough, taking into account all relevant aspects of the repository and the different cloud platforms.


GitHub Repository
{GITHUB}

Additional Guidelines
Be specific and detailed in your analysis.
Provide calculations and assumptions used in estimating resources and environmental impact.
Compare and contrast the findings across the three cloud platforms (GCP, AWS, Azure).
Use technical terminology appropriately to convey precision and expertise.
""",
    input_variables=["GITHUB"],
    partial_variables={
        "format_instruction": repo_result_parser.get_format_instructions()
    },
)

calculation_prompt = PromptTemplate(
    template="""As an expert in cloud computing and sustainability, provide a detailed estimation of the hourly power consumption and carbon footprint for the specified instance specs from the leading cloud providers: AWS, GCP, and Azure.

Instructions:
Analyze the instance specifications provided for each cloud provider.
Calculate the hourly power consumption based on the given specs.
Estimate the carbon footprint associated with the hourly power consumption.
Use the most recent data and metrics available for accurate estimations.
Present the results clearly and concisely.
Instance Specifications:
AWS: {aws}

GCP: {gcp}

Azure: {azure}

Desired Format:
{format_instruction}
Ensure that your calculations are accurate and well-documented. Provide references to any data sources or formulas used in the estimation process.
""",
    input_variables=["aws", "gcp", "azure"],
    partial_variables={
        "format_instruction": calculate_result_parser.get_format_instructions()
    },
)


best_instance_prompt = PromptTemplate(
    template="""As an expert in cloud computing economics and environmental sustainability, identify the most economical and environmentally friendly instance among the provided options from AWS, GCP, and Azure.

Instructions:
Analyze the instance specifications and estimation results provided for each cloud provider.
Compare the hourly cost and carbon footprint of each instance.
Determine which instance offers the best balance of cost efficiency and low environmental impact.
Clearly explain the reasoning behind your choice, supported by data.

Instance Specifications and Estimation Results:

AWS: {aws}

GCP: {gcp}

Azure: {azure}

Desired Format:
{format_instruction}

Ensure that your analysis is thorough and well-documented. Provide references to any data sources or formulas used in the estimation process.
""",
    input_variables=["aws", "gcp", "azure"],
    partial_variables={
        "format_instruction": best_instance_parser.get_format_instructions()
    },
)

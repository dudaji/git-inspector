from langchain.prompts import PromptTemplate
from functions.analyzer.parser import output_parser

prompt = PromptTemplate(
    template="""
As an expert in analyzing software repositories and estimating resource consumption and environmental impact, your task is to provide a comprehensive analysis of a GitHub repository.

Instructions
Analyze the structure of the files in the provided GitHub repository by examining the metadata in the documentation.
Identify the entry point of the repository.
Determine the minimum resources required to run the repository on GCP, AWS, and Azure platforms.
Estimate the instance cost, power consumption, and carbon footprint on each platform.
And then get best one among three platforms.
Context
The goal is to gain a detailed understanding of the repository’s requirements and its environmental impact. Your analysis should be thorough, taking into account all relevant aspects of the repository and the different cloud platforms.

Output
Ensure the output is structured in a clear and detailed manner, adhering to the JSON format specified by the following guide: {format_instruction}

GitHub Repository
{GITHUB}

Additional Guidelines
Be specific and detailed in your analysis.
Provide calculations and assumptions used in estimating resources, costs, and environmental impact.
Compare and contrast the findings across the three cloud platforms (GCP, AWS, Azure).
Use technical terminology appropriately to convey precision and expertise.
""",
    input_variables=["GITHUB"],
    partial_variables={"format_instruction": output_parser.get_format_instructions()},
)

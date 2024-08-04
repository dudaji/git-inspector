from pydantic import BaseModel, Field
from typing import Optional
from git_store.model import GitStore

class GitHit(BaseModel):
    repo_url: str = Field(description="The URL requested by the client")
    last_commit: str = Field(description="Estimated Result of Google Cloud Platform(GCP)")
    branch: str
    directory: str
    result: GitStore 

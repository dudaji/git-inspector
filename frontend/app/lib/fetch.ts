
// Default Fetch.
export async function fetchAnalysisData(
  repoUrl?: string,
  branchName?: string,
  directory?: string,
) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  if (repoUrl && branchName) {
    try {
      const body = { repoUrl, branchName, ...(directory && { directory }) };
      const response = await fetch(`${analysisEndpoint}/cache`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze repository");
      }

      return await response.json();
    } catch (err) {
      if (err instanceof Error) {
        return {
          errors: err,
          message: err.message,
        };
      } else {
        return {
          message: "An unknown error occurred",
        };
      }
    }
  }
  return {
    message: "Please insert all fields",
  };
}

// Step-1 Fetch - language distributions
export async function fetchLanguageDistribution(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/language-distribution`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repoUrl }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch language distribution");
    }

    return await response.json();
  } catch (err) {
    if (err instanceof Error) {
      return {
        errors: err,
        message: err.message,
      };
    } else {
      return {
        message: "An unknown error occurred",
      };
    }
  }
}
// Step-2 Fetch - get ResourceRequiremetns
export async function fetchResourceRequirements(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/resource-requirements`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repoUrl }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch resource requirements");
    }

    return await response.json();
  } catch (err) {
    if (err instanceof Error) {
      return {
        errors: err,
        message: err.message,
      };
    } else {
      return {
        message: "An unknown error occurred",
      };
    }
  }
}

// Step-3 Fetch - get costs
export async function fetchRecommendations(
  repoUrl: string,
  cpu: number,
  memory: number,
) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/recommendations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repoUrl, cpu, memory }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch recommendations");
    }

    return await response.json();
  } catch (err) {
    if (err instanceof Error) {
      return {
        errors: err,
        message: err.message,
      };
    } else {
      return {
        message: "An unknown error occurred",
      };
    }
  }
}
// Step-3 Fetch - get costs
export async function fetchCosts(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/costs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repoUrl }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch costs");
    }

    return await response.json();
  } catch (err) {
    if (err instanceof Error) {
      return {
        errors: err,
        message: err.message,
      };
    } else {
      return {
        message: "An unknown error occurred",
      };
    }
  }
}

export async function fetchSummary(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/summary`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ repoUrl }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch summary");
    }

    return await response.json();
  } catch (err) {
    if (err instanceof Error) {
      return {
        errors: err,
        message: err.message,
      };
    } else {
      return {
        message: "An unknown error occurred",
      };
    }
  }
}

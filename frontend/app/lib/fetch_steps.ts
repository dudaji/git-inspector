// Default Fetch - Analyze repository data
export async function fetchAnalysisData(
  repoUrl?: string,
  branchName?: string,
  directory?: string,
) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  if (repoUrl && branchName) {
    try {
      const body = { repoUrl, branchName, ...(directory && { directory }) };
      const response = await fetch(`${analysisEndpoint}/analyze-repo`, {
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

// Step-1 Fetch - Fetch language distribution of the repository
export async function fetchLanguageDistribution(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/analyze-repo`, {
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

// Step-2 Fetch - Get resource requirements of the repository
export async function fetchResourceRequirements(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/analyze-env`, {
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

// Step-3 Fetch - Get instance recommendations based on resource requirements
export async function fetchRecommendations(repoUrl: string, cpu: number, memory: number) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/analyze-instance`, {
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

// Step-3 Fetch - Get costs of the recommended instances
export async function fetchCosts(repoUrl: string) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  try {
    const response = await fetch(`${analysisEndpoint}/analyze-instance`, {
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

// Fetch Summary - Fetch summary of the repository analysis
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

// Cache Fetch - Fetch cached analysis data
export async function fetchCache(repoUrl: string, branchName: string, directory?: string) {
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
        if (response.status === 404) {
          return {
            message: "Cache not found",
          };
        }
        throw new Error("Failed to fetch cache");
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

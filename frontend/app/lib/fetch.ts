export async function fetchAnalysisData(
  repoUrl?: string,
  branchName?: string,
  directory?: string,
) {
  const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;
  if (repoUrl && branchName) {
    try {
      const body = { repoUrl, branchName, ...(directory && { directory }) };
      const response = await fetch(`${analysisEndpoint}`, {
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

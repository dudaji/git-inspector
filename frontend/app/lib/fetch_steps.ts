import { GitBody, EnvBody, AnalyzeInstanceBody } from "@/app/types/model";
const analysisEndpoint = process.env.ANALYSIS_ENDPOINT;

// Default Fetch - Analyze repository data
// - Step 1 API
// - Repository 분석 결과 반환
// - Cloud provider 별 minimum instance spec과 Language Ratio
export async function fetchAnalysisData({ repoUrl, branchName, directory }: GitBody) {
  if (repoUrl && branchName) {
    try {
      console.log("Fecthing to... ", `${analysisEndpoint}/analyze-repo`);
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

// Cache
// - Github 정보를 토대로 이전에 했던 기록이 있으면 기록 결과를 반환하고, 없으면 404에러
export async function fetchCache({ repoUrl, branchName, directory }: GitBody) {
  try {
    console.log("Fecthing to... ", analysisEndpoint);
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

// Step 2 API
// - Minimum instance spec을 보고 전력 소비량과 탄소 배출량 추정
export async function fetchResourceRequirements(envBody: EnvBody) {
  try {
    const response = await fetch(`${analysisEndpoint}/analyze-env`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(envBody),
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

// Step 3 API
// - Minimum Instance spec, 전력 소비량, 탄소 배출량 정보를 토대로 가장 좋은 Instance 선택
export async function fetchRecommendations(analyzeInstanceBody: AnalyzeInstanceBody) {
  try {
    const response = await fetch(`${analysisEndpoint}/analyze-instance`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(analyzeInstanceBody),
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
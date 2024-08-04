import { fileURLToPath } from "url";
import { CloudInstance, Estimate, Scores, DetailedScore } from "@/app/types/model";

export interface CloudProvider {
  instance: CloudInstance;
  estimate: Estimate;
}

// TODO??
export interface Score {
  cost: number;
  performance: number;
  environmentalImpact: number;
  total: number;
}

export function calculateScores(
  results: Record<string, CloudProvider>,
): [string, Record<string, Score>] {
  const { conclusion, language_ratio, ...filtered } = results;
  const scores: Record<string, Score> = {};
  const costs = Object.values(filtered).map((p) => p.instance.costPerHour);
  const cpus = Object.values(filtered).map((p) => p.instance.cpu);
  const memories = Object.values(filtered).map((p) => p.instance.ram);
  const carbonFootprints = Object.values(filtered).map((p) =>
    parseFloat(p.estimate.carbonFootprint.split(" ")[0]),
  );

  const minCost = Math.min(...costs);
  const maxCost = Math.max(...costs);
  const maxCPU = Math.max(...cpus);
  const maxMemory = Math.max(...memories);
  const minCarbon = Math.min(...carbonFootprints);
  const maxCarbon = Math.max(...carbonFootprints);

  for (const [name, provider] of Object.entries(filtered)) {
    const cost = provider.instance.costPerHour;
    const cpu = provider.instance.cpu;
    const memory = provider.instance.ram;
    const carbonFootprint = parseFloat(
      provider.estimate.carbonFootprint.split(" ")[0],
    );
    const hasGPU =
      provider.instance.gpu != null && provider.instance.gpu !== "None";

    const costScore = 40 - ((cost - minCost) / (maxCost - minCost)) * 30;

    const cpuScore = (cpu / maxCPU) * 10;
    const memoryScore = (memory / maxMemory) * 10;
    let gpuScore = 0;
    if (hasGPU) {
      gpuScore = 10;
    }
    const performanceScore = cpuScore + memoryScore + gpuScore;

    const environmentalImpactScore =
      30 - ((carbonFootprint - minCarbon) / (maxCarbon - minCarbon)) * 20;

    const totalScore = costScore + performanceScore + environmentalImpactScore;

    scores[name] = {
      cost: costScore,
      performance: performanceScore,
      environmentalImpact: environmentalImpactScore,
      total: totalScore,
    };
  }

  const winner = Object.keys(scores).reduce((maxKey, key) => {
    return scores[key].total > scores[maxKey].total ? key : maxKey;
  }, Object.keys(scores)[0]);

  return [winner, scores];
}



// 새로 추가된 최소 비용 인스턴스 반환 함수
export function getMinInstanceCost(
  results: Record<string, CloudProvider>,
): [string, CloudInstance] {
  const { conclusion, languageRatio, ...filtered } = results;
  const costs = Object.values(filtered).map((p) => p.instance.costPerHour);

  const minCost = Math.min(...costs);

  for (const [name, provider] of Object.entries(filtered)) {
    if (provider.instance.costPerHour === minCost) {
      return [name, provider.instance];
    }
  }

  throw new Error("No minimum cost instance found");
}
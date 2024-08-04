import { fileURLToPath } from "url";

export interface CloudProvider {
  instance: {
    cpu: number;
    description: string;
    cloudProvider: string;
    ram: number;
    costPerHour: number;
    storage: number;
    gpu: string | null;
    region: string;
    name: string;
  };
  estimate: {
    carbonFootprint: string;
    description: string;
    powerConsumption: string;
  };
}

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

export interface CloudProvider {
  instance: {
    cpu: number;
    description: string;
    cloud_provider: string;
    ram: number;
    cost_per_hour: number;
    storage: number;
    gpu: string | null;
    region: string;
    name: string;
  };
  estimate: {
    carbon_footprint: string;
    description: string;
    power_consumption: string;
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

  const costs = Object.values(filtered).map((p) => p.instance.cost_per_hour);
  const cpus = Object.values(filtered).map((p) => p.instance.cpu);
  const memories = Object.values(filtered).map((p) => p.instance.ram);
  const carbonFootprints = Object.values(filtered).map((p) =>
    parseFloat(p.estimate.carbon_footprint.split(" ")[0]),
  );

  const minCost = Math.min(...costs);
  const maxCost = Math.max(...costs);
  const maxCPU = Math.max(...cpus);
  const maxMemory = Math.max(...memories);
  const minCarbon = Math.min(...carbonFootprints);
  const maxCarbon = Math.max(...carbonFootprints);

  for (const [name, provider] of Object.entries(filtered)) {
    const cost = provider.instance.cost_per_hour;
    const cpu = provider.instance.cpu;
    const memory = provider.instance.ram;
    const carbonFootprint = parseFloat(
      provider.estimate.carbon_footprint.split(" ")[0],
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

export interface CloudProvider {
  instance: {
    cpu: string;
    memory: string;
    gpu: string;
  };
  pricing: {
    // monthly: string;
    cost_per_hour: string;
  };
  carbon_footprint: {
    monthly: string;
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
  const { conclusion, ...filtered } = results;
  const scores: Record<string, Score> = {};

  const costs = Object.values(filtered).map((p) =>
    // parseFloat(p.pricing.monthly.replace("$", "")),
    parseFloat(p.pricing.cost_per_hour.replace("$", "")),
  );
  const cpus = Object.values(filtered).map((p) =>
    parseInt(p.instance.cpu.split(" ")[0]),
  );
  const memories = Object.values(filtered).map((p) =>
    parseFloat(p.instance.memory.split(" ")[0]),
  );
  const carbonFootprints = Object.values(filtered).map((p) =>
    parseFloat(p.carbon_footprint.monthly.split(" ")[0]),
  );

  const minCost = Math.min(...costs);
  const maxCost = Math.max(...costs);
  const maxCPU = Math.max(...cpus);
  const maxMemory = Math.max(...memories);
  const minCarbon = Math.min(...carbonFootprints);
  const maxCarbon = Math.max(...carbonFootprints);

  for (const [name, provider] of Object.entries(filtered)) {
    const cost = parseFloat(provider.pricing.cost_per_hour.replace("$", ""));
    const cpu = parseInt(provider.instance.cpu.split(" ")[0]);
    const memory = parseFloat(provider.instance.memory.split(" ")[0]);
    const carbonFootprint = parseFloat(
      provider.carbon_footprint.monthly.split(" ")[0],
    );
    const hasGPU = provider.instance.gpu != "None";

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

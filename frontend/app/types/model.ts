export interface CloudInstance {
  cloudProvider: string;
  name: string;
  cpu: number;
  ram: number;
  storage: number;
  gpu: string | null;
  region: string;
  costPerHour: number;
  description: string;
}

export interface RepoResult {
  gcp: CloudInstance;
  aws: CloudInstance;
  azure: CloudInstance;
  languageRatio: Record<string, number>;
}

export interface Estimate {
  powerConsumption: string;
  carbonFootprint: string;
  description: string;
}

export interface CalculateResult {
  gcp: Estimate;
  aws: Estimate;
  azure: Estimate;
}

export interface InstanceResult {
  instance: CloudInstance;
  estimate: Estimate;
}

export interface FinalResponse {
  aws: InstanceResult;
  gcp: InstanceResult;
  azure: InstanceResult;
  conclusion: InstanceResult;
  languageRatio: Record<string, number>;
}

export interface DetailedScore {
  cost_efficiency: number;
  performance: number;
  environmental_impact: number;
  total: number;
}

export interface Scores {
  winner: string;
  gcp: DetailedScore;
  aws: DetailedScore;
  azure: DetailedScore;
  language: number;
}

export interface GeminiAnalysis {
  repo_url: string;
  branch: string;
  directory: string;
  result: Record<string, any>;
  scores: Scores;
}

export interface CloudProvider {
  instance: CloudInstance;
  estimate: Estimate;
}
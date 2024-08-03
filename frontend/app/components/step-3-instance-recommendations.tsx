import { fetchRecommendations } from '@/app/lib/fetch';

export async function InstanceRecommendations({ repoUrl, cpu, memory }: { repoUrl: string, cpu: number, memory: number }) {
  const recommendations = await fetchRecommendations(repoUrl, cpu, memory);

  return (
    <div>
      <h2>Recommendations</h2>
      {Object.keys(recommendations).map(provider => (
        <div key={provider}>
          <h3>{provider.toUpperCase()}</h3>
          <p>{recommendations[provider].instanceSpec}</p>
        </div>
      ))}
    </div>
  );
}
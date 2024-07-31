import { fetchAnalysisData } from "@/app/lib/fetch";
import { calculateScores } from "@/app/lib/score";
import CloudScoreCard from "./cloud-score-card";

interface CloudInstance {
  name: string;
  cpu: string;
  memory: string;
  gpu: string;
  storage: string;
}
function ConclusionInstance({
  provider,
  instance,
}: {
  provider: string;
  instance: CloudInstance;
}) {
  const formattedProvider =
    provider.charAt(0).toUpperCase() + provider.slice(1).toLowerCase();
  return (
    <div key={`${provider}.${instance.name}`} className="mb-8">
      <h4 className="text-lg font-semibold">{`Recommended ${formattedProvider} Instance Setup`}</h4>
      <table className="table-auto w-full mb-4 mt-4">
        <tbody>
          <tr>
            <td className="border px-4 py-2">Instance Name</td>
            <td className="border px-4 py-2">{instance.name}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2">CPU</td>
            <td className="border px-4 py-2">{instance.cpu}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Memory</td>
            <td className="border px-4 py-2">{instance.memory}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Storage</td>
            <td className="border px-4 py-2">{instance.storage}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2">GPU</td>
            <td className="border px-4 py-2">{instance.gpu}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default async function AnalysisResults({
  repoUrl,
  branchName,
  directory,
}: {
  repoUrl?: string;
  branchName?: string;
  directory?: string;
}) {
  const result = await fetchAnalysisData(repoUrl, branchName, directory);

  if (result?.message) {
    return (
      <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
        {`ERROR: ${result.message}`}
      </div>
    );
  }

  if (Object.keys(result).length == 0) {
    return <p>No results available.</p>;
  }

  const [winner, scores] = calculateScores(result);

  return (
    <div>
      {Object.entries(scores)
        .sort((a, b) => b[1].total - a[1].total)
        .map(([providerName, score]) => (
          <CloudScoreCard
            key={providerName}
            provider={providerName}
            winner={providerName == winner}
            score={score}
          />
        ))}

      <ConclusionInstance
        provider={winner}
        instance={result[winner].instance}
      />
      <p>{result["conclusion"].description}</p>
    </div>
  );
}

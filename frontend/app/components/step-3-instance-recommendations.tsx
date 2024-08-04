import { fetchAnalysisData } from '@/app/lib/fetch';
import { calculateScores } from "@/app/lib/score";
import CloudScoreCard from "./cloud-cost-card";
import React, { useState } from "react";

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
  onClick,
}: {
  provider: string;
  instance: CloudInstance;
  onClick: () => void;
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
      <button onClick={onClick} className="mt-4 text-blue-500 underline">
        Show detailed comparison
      </button>
    </div>
  );
}

export default async function InstanceRecommendations({
  repoUrl,
  branchName,
  directory,
}: {
  repoUrl?: string;
  branchName?: string;
  directory?: string;
}) {
  const result = await fetchAnalysisData(repoUrl, branchName, directory);
  const [showDetails, setShowDetails] = useState(false);

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

  const conclusionProvider = winner; // or fetch from result.conclusion.provider
  const conclusionInstance = result.conclusion.instance;

  return (
    <div>
      <ConclusionInstance
        provider={conclusionProvider}
        instance={conclusionInstance}
        onClick={() => setShowDetails(true)}
      />
      <p>{result.conclusion.description}</p>
      {showDetails && (
        <div>
          {Object.keys(result).map(provider => (
            <CloudScoreCard
              key={provider}
              provider={provider}
              score={result[provider].score}
              winner={provider === conclusionProvider}
            />
          ))}
        </div>
      )}
    </div>
  );
}

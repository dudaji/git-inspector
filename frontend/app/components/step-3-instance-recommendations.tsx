import { getMinInstanceCost } from "@/app/lib/score";
import CloudScoreCard from "./cloud-cost-card";
import React, { useState } from "react";
import { Modal } from "@/app/components/ui/modal";
import { CloudInstance } from "@/app/types/model";

interface CloudInstanceProps {
  provider: string;
  instance: CloudInstance;
  onClick: () => void;
}

function ConclusionInstance({
  provider,
  instance,
  onClick,
}: CloudInstanceProps) {
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
            <td className="border px-4 py-2">{instance.ram}</td>
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

const InstanceRecommendations = ({
  recommendationData,
}: {
  recommendationData: any;
}) => {
  const [showDetails, setShowDetails] = useState(false);

  if (recommendationData?.message) {
    return (
      <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
        {`ERROR: ${recommendationData.message}`}
      </div>
    );
  }

  if (!recommendationData || Object.keys(recommendationData).length === 0) {
    return <p>No results available.</p>;
  }

  console.log("How recommendation looks?", recommendationData)
  const [winner, instance] = getMinInstanceCost(recommendationData);
  const conclusionProvider = winner;
  const conclusionInstance: CloudInstance = {
    cloudProvider: conclusionProvider,
    name: instance.name,
    cpu: instance.cpu,
    ram: instance.ram,
    storage: instance.storage,
    gpu: instance.gpu,
    region: instance.region,
    costPerHour: instance.costPerHour,
    description: instance.description
  };

  return (
    <div>
      <ConclusionInstance
        provider={conclusionProvider}
        instance={conclusionInstance}
        onClick={() => setShowDetails(true)}
      />
      <p>{recommendationData.conclusion.description}</p>
      <Modal isVisible={showDetails} onClose={() => setShowDetails(false)}>
        {Object.keys(recommendationData).map(provider => (
          <CloudScoreCard
            key={provider}
            provider={provider}
            score={recommendationData[provider].score}
            winner={provider === conclusionProvider}
          />
        ))}
      </Modal>
    </div>
  );
};

export default InstanceRecommendations;
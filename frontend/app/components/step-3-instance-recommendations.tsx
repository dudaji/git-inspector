"use client"; // 클라이언트 컴포넌트로 지정

import React, { useState } from "react";
import { Modal } from "@/app/components/ui/modal";
import { CloudInstance, InstanceResult , RepoResult} from "@/app/types/model";

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
    provider.toUpperCase();
  return (
    <div key={`${provider}.${instance.name}`} className="mb-8 text-center">
      <h4 className="text-lg font-semibold">{`${formattedProvider.toUpperCase()}`}</h4>
      <table className="table-auto w-full mb-4 mt-4">
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/2">Instance Name</td>
            <td className="border px-4 py-2 w-1/2">{instance.name}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">CPU</td>
            <td className="border px-4 py-2 w-1/2">{instance.cpu}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">Memory</td>
            <td className="border px-4 py-2 w-1/2">{instance.ram}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">Cost per Hour</td>
            <td className="border px-4 py-2 w-1/2">{instance.costPerHour}</td>
          </tr>
        </tbody>
      </table>
      <button onClick={onClick} className="mt-4 text-blue-500 underline">
        Show ALL
      </button>
    </div>
  );
}

const InstanceRecommendations = ({
  recommendationData, analysisData
}: {
  recommendationData: InstanceResult;
  analysisData: RepoResult;
}) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!recommendationData || Object.keys(recommendationData).length === 0) {
    return <p>No results available.</p>;
  }

  // console.log("How recommendation looks?", recommendationData);
  const conclusionInstance: CloudInstance = recommendationData.instance;
  // console.log("Get anaylsis data from previous page:", analysisData);
  return (
    <div>
      <ConclusionInstance
        provider={conclusionInstance.cloudProvider}
        instance={conclusionInstance}
        onClick={() => setShowDetails(true)}
      />
      <Modal isVisible={showDetails} onClose={() => setShowDetails(false)}>
        {Object.keys(analysisData).map((provider) => {
          if (provider === 'languageRatio') return null;
          const instance = analysisData[provider as keyof RepoResult];
          return (
            <div key={provider} className="p-4">
              <h4 className="text-xl font-semibold text-center">{`${provider.toUpperCase()}`}</h4>
              <table className="table-auto w-full mb-4 mt-4">
                <tbody>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Instance Name</td>
                    <td className="border px-4 py-2 w-1/2">{instance.name}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">CPU</td>
                    <td className="border px-4 py-2 w-1/2">{instance.cpu}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Memory</td>
                    <td className="border px-4 py-2 w-1/2">{instance.ram}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Cost per Hour</td>
                    <td className="border px-4 py-2 w-1/2">{instance.costPerHour} $</td>
                  </tr>
                </tbody>
              </table>
            </div>
          );
        })}
      </Modal>
    </div>
  );
};

export default InstanceRecommendations;
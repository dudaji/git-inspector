"use client"; // 클라이언트 컴포넌트로 지정

import React, { useState } from "react";
import { calculateScores, Score } from "@/app/lib/score";
import CloudScoreCard from "./cloud-cost-card";
import { Modal } from "@/app/components/ui/modal";
import { CloudInstance, InstanceResult , RepoResult} from "@/app/types/model";

interface CloudInstanceProps {
  provider: string;
  instance: CloudInstance;
  estimate: {
    powerConsumption: string;
    carbonFootprint: string;
    description: string;
  };
  onClick: () => void;
}


function ConclusionInstance({
  provider,
  instance,
  estimate,
  onClick,
}: CloudInstanceProps) {
  const formattedProvider =
    provider.toUpperCase();
  return (
    <div key={`${provider}.${instance.name}`} className="mb-8 text-center">
      <h4 className="text-lg font-semibold">{`Recommended ${formattedProvider}`}</h4>
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
            <td className="border px-4 py-2">Power Consumption</td>
            <td className="border px-4 py-2">{estimate.powerConsumption}</td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Carbon Footprint</td>
            <td className="border px-4 py-2">{estimate.carbonFootprint}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

const CloudCostInstances = ({
  recommendationData,
  analysisData,
}: {
  recommendationData: InstanceResult;
  analysisData: RepoResult;
}) => {
  // const [showScoreList, setShowScoreList] = useState(false);
  // const [showDetails, setShowDetails] = useState(false);

  if (!recommendationData || Object.keys(recommendationData).length === 0) {
    return <p>No results available.</p>;
  }

  function getMaxTotalScore(scores: Record<string, Score>): string {
    let maxTotalScore: Score | null = null;
    let maxKey: string = "";
  
    for (const key in scores) {
      if (scores.hasOwnProperty(key)) {
        const score = scores[key];
        if (maxTotalScore === null || score.total > maxTotalScore.total) {
          maxTotalScore = score;
          maxKey = key;
        }
      }
    }
  
    return maxKey
  }
  

  const transformedAnalysisData: Record<string, InstanceResult> = {
    gcp: {
      instance: analysisData.gcp,
      estimate: {
        powerConsumption: "",
        carbonFootprint: "",
        description: "",
      },
    },
    aws: {
      instance: analysisData.aws,
      estimate: {
        powerConsumption: "",
        carbonFootprint: "",
        description: "",
      },
    },
    azure: {
      instance: analysisData.azure,
      estimate: {
        powerConsumption: "",
        carbonFootprint: "",
        description: "",
      },
    },
  };

  const [winner, scores] = calculateScores(transformedAnalysisData);
  console.log("Get winner and scoes: ", winner, scores)
  const bestProviderName = getMaxTotalScore(scores)
  return (
    <div>
      <CloudScoreCard
        key={bestProviderName}
        provider={bestProviderName}
        winner={bestProviderName === winner}
        score={scores[bestProviderName]}
      />
      {/* <button onClick={() => {setShowScoreList(true)}} className="mt-4 text-blue-500 underline">
        Show All Scores
      </button>
      <Modal isVisible={showScoreList} onClose={() => setShowScoreList(false)}>
        {Object.entries(scores).map(([providerName, score]) => {
          return (<CloudScoreCard 
            key={`${providerName}-modal`}
            provider={providerName}
            winner={bestProviderName === winner}
            score={score}
          />)
        })}
      </Modal>
      <ConclusionInstance
        provider={winner}
        instance={transformedAnalysisData[winner].instance}
        estimate={transformedAnalysisData[winner].estimate}
        onClick={() => setShowDetails(true)}
      />
       <Modal isVisible={showDetails} onClose={() => setShowDetails(false)}>
        {Object.keys(transformedAnalysisData).map((provider) => {
          if (provider === 'languageRatio') return null;
          const data = transformedAnalysisData[provider];
          return (
            <div key={provider} className="p-4">
              <h4 className="text-xl font-semibold text-center">{`${provider.toUpperCase()}`}</h4>
              <table className="table-auto w-full mb-4 mt-4">
                <tbody>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Instance Name</td>
                    <td className="border px-4 py-2 w-1/2">{data.instance.name}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">CPU</td>
                    <td className="border px-4 py-2 w-1/2">{data.instance.cpu}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Memory</td>
                    <td className="border px-4 py-2 w-1/2">{data.instance.ram}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Power Consumption</td>
                    <td className="border px-4 py-2 w-1/2">{data.estimate.powerConsumption}</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2 w-1/2">Carbon Footprint</td>
                    <td className="border px-4 py-2 w-1/2">{data.estimate.carbonFootprint}</td>
                  </tr>
                </tbody>
              </table>
              <p className="mb-4">{data.estimate.description}</p>
            </div>
          );
        })}
      </Modal> */}
    </div>
  );
};

export default CloudCostInstances;
"use client"; // 클라이언트 컴포넌트로 지정

import React, { useState } from "react";
import { calculateScores, Score } from "@/app/lib/score";
import CloudScoreCard from "./cloud-cost-card";
import { Modal } from "@/app/components/ui/modal";
import { Button } from "./ui/button";
import { Estimate, InstanceResult , RepoResult, CloudInstance} from "@/app/types/model";

interface CloudCostInstancesWithDataProps {
  recommendationData: {
    aws: Estimate;
    gcp: Estimate;
    azure: Estimate;
    recommendation: InstanceResult;
  };
  analysisData: RepoResult;
}

const CloudCostInstancesWithData = ({
  recommendationData,
  analysisData,
}: CloudCostInstancesWithDataProps) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!recommendationData || Object.keys(recommendationData).length === 0) {
    return <p>No results available.</p>;
  }

  const transformedAnalysisData: Record<string, InstanceResult> = {
    gcp: {
      instance: analysisData.gcp,
      estimate: recommendationData.gcp,
    },
    aws: {
      instance: analysisData.aws,
      estimate: recommendationData.aws,
    },
    azure: {
      instance: analysisData.azure,
      estimate: recommendationData.azure,
    },
  };
  
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
  
    return maxKey;
  }

  const [winner, scores] = calculateScores(transformedAnalysisData);
  const bestProviderName = getMaxTotalScore(scores);

  return (
    <div>
      <CloudScoreCard
        key={bestProviderName}
        provider={bestProviderName}
        winner={bestProviderName === winner}
        score={scores[bestProviderName]}
      />
      <div className="w-full flex justify-center"> {/* 부모 div를 사용하여 중앙 정렬 */}
          <Button
            onClick={() => setShowDetails(true)}
            className="w-2/3"
          >
            Show all
          </Button>
        </div>
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
      </Modal>
    </div>
  );
};

export default CloudCostInstancesWithData;
"use client"; // 클라이언트 컴포넌트로 지정

import React, { useState } from "react";
import { Modal } from "@/app/components/ui/modal";
import { CloudInstance, InstanceResult , RepoResult} from "@/app/types/model";
import { Button } from "@/app/components/ui/button";
import InstanceRecommendCard from "@/app/components/instance-recommend-card";
const InstanceRecommendations = ({
  recommendationData,
  analysisData,
}: {
  recommendationData: InstanceResult;
  analysisData: RepoResult;
}) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!recommendationData || Object.keys(recommendationData).length === 0) {
    return <p>No results available.</p>;
  }

  const conclusionInstance: CloudInstance = recommendationData.instance;

  return (
    <div>
      <InstanceRecommendCard
        provider={conclusionInstance.cloudProvider}
        instance={conclusionInstance}
        winner={true}
      />
    
      <div className="w-full flex justify-center"> {/* 부모 div를 사용하여 중앙 정렬 */}
          <Button
            onClick={() => setShowDetails(true)}
            className="w-2/3"
          >
            Show all Instances
          </Button>
        </div>
      <Modal isVisible={showDetails} onClose={() => setShowDetails(false)}>
        {Object.keys(analysisData).map((provider) => {
          if (provider === 'languageRatio') return null;
          const instance = analysisData[provider as keyof RepoResult];
          return (
            <InstanceRecommendCard
              key={provider}
              provider={provider}
              instance={instance as CloudInstance}
              winner={false}
            />
          );
        })}
      </Modal>
    </div>
  );
};

export default InstanceRecommendations;
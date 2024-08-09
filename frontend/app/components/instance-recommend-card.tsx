import React from "react";
import { CloudInstance } from "@/app/types/model";

interface InstanceRecommendCardProps {
  provider: string;
  instance: CloudInstance;
  winner: boolean;
}

const InstanceRecommendCard: React.FC<InstanceRecommendCardProps> = ({
  provider,
  instance,
  winner,
}) => {
  const cardStyle = {
    backgroundColor: winner ? "var(--winner)" : "var(--background)",
    borderColor: winner ? "var(--winner-border)" : "var(--border)",
    borderWidth: winner ? "4px" : "1px",
  };

  const instanceDetails = [
    { name: "Instance Name", value: instance.name },
    { name: "CPU", value: instance.cpu },
    { name: "Memory", value: instance.ram },
    { name: "Region", value: instance.region },
    {
      name: "Cost per Hour",
      value: `${Number(instance.costPerHour).toPrecision(3)} $`,
    },
  ];

  return (
    <div style={cardStyle} className={`p-6 mb-6 rounded-lg shadow-lg`}>
      <h2 className="text-2xl font-bold mb-4">
        {provider.toUpperCase()}
        {winner && (
          <span className="ml-2 bg-secondary text-sm font-bold px-2 py-1 rounded">
            Winner 🏆
          </span>
        )}
      </h2>
      <div className="space-y-4">
        {instanceDetails.map((detail) => (
          <div
            key={detail.name}
            className="flex justify-between items-center mb-1"
          >
            <span className="text-lg font-medium text-gray-700">
              {detail.name}
            </span>
            <span className="text-lg font-medium text-gray-700">
              {detail.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InstanceRecommendCard;

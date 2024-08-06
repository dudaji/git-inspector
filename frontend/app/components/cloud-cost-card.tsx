import React from "react";
import { Score } from "@/app/lib/score";

interface CloudScoreCardProps {
  provider: string;
  score: Score;
  winner: boolean;
}

const CloudScoreCard: React.FC<CloudScoreCardProps> = ({
  provider,
  score,
  winner,
}) => {
  const scoreCategories = [
    { name: "Cost Efficiency", value: score.cost },
    { name: "Performance", value: score.performance },
    { name: "Environmental Impact", value: score.environmentalImpact },
  ];
  const cardStyle = {
    backgroundColor: winner ? "var(--winner)" : "var(--background)",
    borderColor: winner ? "var(--winner-border)" : "var(--border)",
    borderWidth: winner ? "4px" : "1px",
  };

  return (
    <div style={cardStyle} className={`p-6 mb-6 rounded-lg shadow-lg `}>
      <h2 className="text-2xl font-bold mb-4">
        {provider.toUpperCase()}
        {winner && (
          <span className="ml-2 bg-secondary text-white text-sm font-bold px-2 py-1 rounded">
            Winner 🏆
          </span>
        )}
      </h2>
      <div className="space-y-4">
        {scoreCategories.map((category) => (
          <div key={category.name}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm font-medium text-gray-700">
                {category.name}
              </span>
              <span className="text-sm font-medium text-gray-700">
                {category.value.toFixed(2)}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full"
                style={{ width: `${(category.value / 30) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6">
        <div className="flex justify-between items-center mb-1">
          <span className="text-lg font-bold text-gray-700">Total Score</span>
          <span className="text-lg font-bold text-gray-700">
            {score.total.toFixed(2)}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-green-600 h-3 rounded-full"
            style={{ width: `${(score.total / 100) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default CloudScoreCard;

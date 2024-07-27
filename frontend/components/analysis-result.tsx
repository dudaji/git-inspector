"use client";

import { CardContent } from "@/components/ui/card";
import { useEffect, useState } from "react";

export default function AnalysisResults({
  repoUrl,
  branchName,
}: {
  repoUrl: string;
  branchName: string;
}) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{
    power: string;
    carbon: string;
    cost: string;
  } | null>(null);

  useEffect(() => {
    if (repoUrl && branchName) {
      const fetchData = async () => {
        try {
          const response = await fetch("/api/analyze-repo", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ repoUrl, branchName }),
          });

          if (!response.ok) {
            throw new Error("Failed to analyze repository");
          }

          const data = await response.json();
          setResult(data.predictions);
          setLoading(false);
        } catch (err) {
          setLoading(false);
          if (err instanceof Error) {
            setError("Error: " + err.message);
          } else {
            setError("An unknown error occurred");
          }
        }
      };

      fetchData();
    }
  }, [repoUrl, branchName]);

  return (
    <CardContent className="space-y-4">
      {loading ? (
        <div className="flex flex-col items-center justify-center py-8 space-y-4">
          <div className="h-8 w-8 animate-spin" />
          <div className="text-muted-foreground">Loading...</div>
          <div className="text-sm text-muted-foreground">
            This may take a few seconds...
          </div>
        </div>
      ) : error ? (
        <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
          {error}
        </div>
      ) : result ? (
        <div>
          <h3 className="text-xl font-semibold">Predictions:</h3>
          <p>Power: {result.power}</p>
          <p>Carbon: {result.carbon}</p>
          <p>Cost: {result.cost}</p>
        </div>
      ) : (
        <p>No results available.</p>
      )}
    </CardContent>
  );
}

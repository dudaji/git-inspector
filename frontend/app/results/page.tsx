import React, { Suspense } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/app/components/ui/card";
// import LanguageDistribution from "@/app/components/step-1-language-distribution";
import { LanguageDistribution } from "@/app/components/step-1-language-distribution";
import { ResourceRequirements } from "@/app/components/step-2-resource-requirements";
import InstanceRecommendationsWithData from "@/app/components/step-3-instance-recommendations";
import CloudCostInstancesWithData from "@/app/components/step-4-cloud-cost-winner";
import Link from "next/link";
import { Button } from "@/app/components/ui/button";
import { LoadingComponent } from "@/app/components/ui/loading";
import {
  fetchAnalysisData,
  fetchCache,
  fetchResourceRequirements,
  fetchRecommendations,
} from "@/app/lib/fetch";
import {
  GitBody,
  Estimate,
  AnalyzeInstanceBody,
  InstanceResult,
  CloudInstance,
  FinalResponse,
} from "@/app/types/model";

type SearchParams = {
  repoUrl?: string;
  branchName?: string;
  directory?: string;
};

async function LatestResults({ analysisData }: { analysisData: any }) {
  console.log("get data from before steps:", analysisData);
  const resourceRequirements = await fetchResourceRequirements({
    aws: analysisData.aws as CloudInstance,
    gcp: analysisData.gcp as CloudInstance,
    azure: analysisData.azure as CloudInstance,
    hash_id: analysisData.hash_id,
  });

  const { hash_id, ...filtered } = analysisData;

  const instanceRecommendation = await fetchRecommendations({
    aws: {
      instance: filtered.aws as CloudInstance,
      estimate: resourceRequirements.aws as Estimate,
    },
    gcp: {
      instance: filtered.gcp as CloudInstance,
      estimate: resourceRequirements.gcp as Estimate,
    },
    azure: {
      instance: filtered.azure as CloudInstance,
      estimate: resourceRequirements.azure as Estimate,
    },
  });

  const completeData = {
    ...resourceRequirements,
    recommendation: instanceRecommendation,
  };

  return (
    <>
      <div className="w-full md:w-1/2 px-2 mt-5">
        <Card className="mb-2 h-full flex flex-col">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-center">
              Cloud Instance Recommendation
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <InstanceRecommendationsWithData
              recommendationData={instanceRecommendation}
              analysisData={filtered}
            />
          </CardContent>
        </Card>
      </div>
      <div className="w-full md:w-1/2 px-2 mt-5">
        <Card className="mb-2 h-full flex flex-col">
          <CardHeader>
            <CardTitle className="text-lg font-bold text-center">
              Instance Scores
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <CloudCostInstancesWithData
              recommendationData={completeData}
              analysisData={filtered}
            />
          </CardContent>
        </Card>
      </div>
    </>
  );
}

export default async function ResultsPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const encodedRepoUrl = encodeURIComponent(searchParams?.repoUrl || "");
  const encodedBranchName = encodeURIComponent(searchParams?.branchName || "");
  const encodedDirectory = encodeURIComponent(searchParams?.directory || "");
  const detailedPagePath =
    `/results-detail?repoUrl=${encodedRepoUrl}&branchName=${encodedBranchName}` +
    (encodedDirectory ? `&directory=${encodedDirectory}` : "");

  const repoUrl = searchParams?.repoUrl || "N/A";
  const branchName = searchParams?.branchName || "N/A";
  const gitBody: GitBody = {
    repoUrl,
    branchName,
    directory: searchParams?.directory || "",
  };

  const analysisData = await fetchAnalysisData(gitBody);
  const hashKey = analysisData?.hash_id;

  return (
    <div className="mx-auto max-w-6xl p-4 bg-background border rounded-lg">
      <CardHeader>
        <CardTitle className="text-xl font-bold">
          Analysis Results of branch
          <span style={{ color: "hsl(var(--accent))" }}> {branchName} </span>
          in
          <span style={{ color: "hsl(var(--accent))" }}> {repoUrl}</span>
        </CardTitle>
      </CardHeader>
      <div className="flex flex-wrap -mx-2">
        <div className="w-full md:w-1/2 px-2">
          <Card className="mb-2 h-full flex flex-col">
            <CardHeader>
              <CardTitle className="text-lg font-bold text-center">
                Language Distribution
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-grow">
              <LanguageDistribution data={analysisData} />
            </CardContent>
          </Card>
        </div>
        <div className="w-full md:w-1/2 px-2">
          <Card className="mb-2 h-full flex flex-col">
            <CardHeader>
              <CardTitle className="text-lg font-bold text-center">
                Resource Requirements
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-grow">
              <ResourceRequirements data={analysisData} />
            </CardContent>
          </Card>
        </div>
        <Suspense fallback={<LoadingComponent />}>
          <LatestResults analysisData={analysisData} />
        </Suspense>
      </div>
    </div>
  );
}


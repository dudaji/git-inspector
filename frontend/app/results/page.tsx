import React, { Suspense } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/app/components/ui/card";
import { LanguageDistribution } from "@/app/components/step-1-language-distribution";
import { ResourceRequirements } from "@/app/components/step-2-resource-requirements";
import InstanceRecommendationsWithData from "@/app/components/step-3-instance-recommendations";
import CloudCostInstancesWithData from "@/app/components/step-4-cloud-cost-winner";
import { LoadingComponent } from "@/app/components/ui/loading";
import {
  fetchAnalysisData,
  fetchResourceRequirements,
  fetchRecommendations,
} from "@/app/lib/fetch";
import { GitBody, CloudInstance, Estimate } from "@/app/types/model";

type SearchParams = {
  repoUrl?: string;
  branchName?: string;
  directory?: string;
};

function SuspenseCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="w-full md:w-1/2 px-2 mt-5">
      <Card className="mb-2 h-full flex flex-col">
        <CardHeader>
          <CardTitle className="text-lg font-bold text-center">
            {title}
          </CardTitle>
        </CardHeader>
        <Suspense
          fallback={
            <CardContent className="flex-grow flex items-center justify-center">
              <LoadingComponent />
            </CardContent>
          }
        >
          <CardContent className="flex-grow">{children}</CardContent>
        </Suspense>
      </Card>
    </div>
  );
}

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
      <SuspenseCard title="Cloud Instance Recommendation">
        <InstanceRecommendationsWithData
          recommendationData={instanceRecommendation}
          analysisData={filtered}
        />
      </SuspenseCard>
      <SuspenseCard title="Instance Scores">
        <CloudCostInstancesWithData
          recommendationData={completeData}
          analysisData={filtered}
        />
      </SuspenseCard>
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

  const repoUrl = searchParams?.repoUrl || "N/A";
  const branchName = searchParams?.branchName || "N/A";
  const gitBody: GitBody = {
    repoUrl,
    branchName,
    directory: searchParams?.directory || "",
  };

  const analysisData = await fetchAnalysisData(gitBody);

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
        <LatestResults analysisData={analysisData} />
      </div>
    </div>
  );
}

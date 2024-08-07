import React, { Suspense } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/app/components/ui/card";
// import LanguageDistribution from "@/app/components/step-1-language-distribution";
import { LanguageDistribution } from "@/app/components/step-1-language-distribution";
import { ResourceRequirements } from "@/app/components/step-2-resource-requirements";
import InstanceRecommendationsWithData from "@/app/components/step-3-instance-recommendations";
import CloudCostInstancesWithData from "@/app/components/step-4-cloud-cost-winner";
import Link from "next/link";
import { Button } from "@/app/components/ui/button";
import { LoadingComponent } from "@/app/components/ui/loading";
import { fetchAnalysisData, fetchCache, fetchResourceRequirements, fetchRecommendations } from "@/app/lib/fetch";
import { GitBody, Estimate, AnalyzeInstanceBody, InstanceResult, CloudInstance , FinalResponse} from "@/app/types/model";

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
  });

  const instanceRecommendation = await fetchRecommendations({
    aws: {
      instance: analysisData.aws as CloudInstance,
      estimate: resourceRequirements.aws as Estimate,
    },
    gcp: {
      instance: analysisData.gcp as CloudInstance,
      estimate: resourceRequirements.gcp as Estimate,
    },
    azure: {
      instance: analysisData.azure as CloudInstance,
      estimate: resourceRequirements.azure as Estimate,
    },
  });

  const completeData = {
    ...resourceRequirements,
    recommendation: instanceRecommendation
  };


  return (
    <>
      <div className="w-full md:w-1/2 px-2 mt-5">
        <Card className="mb-4 h-full flex flex-col">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-center">
              Cloud Instance Recommendation
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <InstanceRecommendationsWithData 
              recommendationData={instanceRecommendation} 
              analysisData={analysisData} 
            />
          </CardContent>
        </Card>
      </div>
      <div className="w-full md:w-1/2 px-2 mt-5">
        <Card className="mb-4 h-full flex flex-col">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-center">
              Instance Scores
            </CardTitle>
          </CardHeader>
            <CardContent className="flex-grow">
            <CloudCostInstancesWithData recommendationData={completeData} analysisData={analysisData} />
            </CardContent>
        </Card>
      </div>
    </>
  );
}

export default async function ResultsPage({ searchParams }: { searchParams: SearchParams }) {
  const encodedRepoUrl = encodeURIComponent(searchParams?.repoUrl || "");
  const encodedBranchName = encodeURIComponent(searchParams?.branchName || "");
  const encodedDirectory = encodeURIComponent(searchParams?.directory || "");
  const detailedPagePath =
    `/results-detail?repoUrl=${encodedRepoUrl}&branchName=${encodedBranchName}` +
    (encodedDirectory ? `&directory=${encodedDirectory}` : "");

  const repoUrl = searchParams?.repoUrl || "N/A";
  const branchName = searchParams?.branchName || "N/A";
  const gitBody: GitBody = { repoUrl, branchName, directory: searchParams?.directory || "" };

  let analysisData;
  try { 
    const cacheData = await fetchCache(gitBody);

    if (cacheData && !cacheData.errors && cacheData.message !== "Cache not found") {
      console.log("Using cached data:", cacheData);
      analysisData = cacheData;
    } else {
      throw new Error("Cache not found or has errors");
     }
    } catch (error) {
      console.log("Fetching analysis data with:", gitBody);
      analysisData = await fetchAnalysisData(gitBody);
      console.log("Fetched analysis data:", analysisData);
    }

  return (
    <div className="mx-auto max-w-7xl p-6 bg-background border">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">
          Analysis Results of branch
          <span style={{ color: "hsl(var(--accent))" }}> {branchName} </span>
          in
          <span style={{ color: "hsl(var(--accent))" }}> {repoUrl}</span>
        </CardTitle>
      </CardHeader>
      <div className="flex flex-wrap -mx-2">
        <div className="w-full md:w-1/2 px-2">
          <Card className="mb-4 h-full flex flex-col">
            <CardHeader>
              <CardTitle className="text-xl font-bold text-center">
                Language Distribution
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-grow"> 
             <LanguageDistribution data={analysisData} />
            </CardContent>
          </Card>
        </div>
        <div className="w-full md:w-1/2 px-2">
          <Card className="mb-4 h-full flex flex-col">
            <CardHeader>
              <CardTitle className="text-xl font-bold text-center">
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
       <div className="w-full flex justify-center">
        <Link href={detailedPagePath}>
          <Button className="mt-6 w-full">Get All LLM Analysis</Button>
        </Link>
        </div>
    </div>
  );
}
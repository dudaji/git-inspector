"use client";

import React, { useEffect, useState } from "react";

import { Card, CardHeader, CardTitle } from "@/app/components/ui/card";
import { Suspense } from "react";
import { LanguageDistribution } from "@/app/components/step-1-language-distribution";
import { ResourceRequirements } from "@/app/components/step-2-resource-requirements";
import { InstanceRecommendations } from "@/app/components/step-3-instance-recommendations";
import CloudCostInstances from "@/app/components/step-4-cloud-cost-winner";
import {} from "@/app/components/cloud-cost-card";
import {} from "@/app/components/step-5-anaylsis-details-llm-summary";
import Link from "next/link";
import { Button } from "@/app/components/ui/button";
import { LoadingComponent } from "../components/ui/loading";
import {
  fetchAnalysisData,
  fetchLanguageDistribution,
  fetchResourceRequirements,
  fetchRecommendations,
  fetchCosts,
  fetchSummary,
  fetchCache,
} from "@/app/lib/fetch_steps"; // Ensure you have these exports in your API file

export default function Results({
  searchParams,
}: {
  searchParams?: {
    repoUrl?: string;
    branchName?: string;
    directory?: string;
  };
}) {
  const [languageData, setLanguageData] = useState(null);
  const [resourceData, setResourceData] = useState(null);
  const [recommendationData, setRecommendationData] = useState(null);
  const [costData, setCostData] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [cacheData, setCacheData] = useState(null);
  const [loading, setLoading] = useState(true);

  const encodedRepoUrl = encodeURIComponent(searchParams?.repoUrl || "");
  const encodedBranchName = encodeURIComponent(searchParams?.branchName || "");
  const encodedDirectory = encodeURIComponent(searchParams?.directory || "");
  const detailedPagePath =
    `/results-detail?repoUrl=${encodedRepoUrl}&branchName=${encodedBranchName}` +
    (encodedDirectory ? `&directory=${encodedDirectory}` : "");

  const repoUrl = searchParams?.repoUrl || "N/A"; // Default to "N/A" if undefined
  const branchName = searchParams?.branchName || "N/A"; // Default to "N/A" if undefined

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const langData = await fetchLanguageDistribution(searchParams?.repoUrl || "");
        setLanguageData(langData);

        const resData = await fetchResourceRequirements(searchParams?.repoUrl || "");
        setResourceData(resData);

        const recData = await fetchRecommendations(searchParams?.repoUrl || "", resData.cpu, resData.memory);
        setRecommendationData(recData);

        const costData = await fetchCosts(searchParams?.repoUrl || "");
        setCostData(costData);

        const sumData = await fetchSummary(searchParams?.repoUrl || "");
        setSummaryData(sumData);

        const cacheData = await fetchCache(searchParams?.repoUrl || "", searchParams?.branchName || "", searchParams?.directory || "");
        setCacheData(cacheData);

      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [searchParams]);

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
          <Suspense fallback={<LoadingComponent />}>
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center">
                  Language Distribution
                </CardTitle>
              </CardHeader>
              <LanguageDistribution
                repoUrl={searchParams?.repoUrl || ""}
                branchName={searchParams?.branchName || ""}
                directory={searchParams?.directory || ""}
              />
            </Card>
          </Suspense>
        </div>
        <div className="w-full md:w-1/2 px-2">
          <Suspense fallback={<LoadingComponent />}>
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center">
                  Resource Requirements
                </CardTitle>
              </CardHeader>
              <ResourceRequirements
                repoUrl={searchParams?.repoUrl || ""}
                branchName={searchParams?.branchName || ""}
                directory={searchParams?.directory || ""}
              />
            </Card>
          </Suspense>
        </div>
        {/* Split here */}
        <div className="w-full md:w-1/2 px-2 mt-5">
          <Suspense fallback={<LoadingComponent />}>
            <Card className="mb-4">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center">
                  {" "}
                  Instance Recommendations
                </CardTitle>
              </CardHeader>
              {/* Show Summary spec of Instances */}
              {/* <CloudCostInstances
                repoUrl={searchParams?.repoUrl}
                branchName={searchParams?.branchName}
                directory={searchParams?.directory}
              /> */}
            </Card>
          </Suspense>
        </div>
        <div className="w-full md:w-1/2 px-2 mt-5">
          <Suspense fallback={<LoadingComponent />}>
            <Card className="mb-4">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center">
                  {" "}
                  Cloud Score Costs
                </CardTitle>
              </CardHeader>
              {/* Show Winner Instance, when Click show all */}
              {/* <CloudCostInstances
                repoUrl={searchParams?.repoUrl}
                branchName={searchParams?.branchName}
                directory={searchParams?.directory}
              /> */}
            </Card>
          </Suspense>
        </div>
      </div>
      <Link href={detailedPagePath}>
        <Button className="mt-6 w-full">Get All LLM Analysis</Button>
      </Link>
    </div>
  );
}


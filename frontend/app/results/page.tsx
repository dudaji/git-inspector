import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/app/components/ui/card";
import AnalysisResults from "@/app/components/analysis-result";
import { Suspense } from "react";
import { LanguageDistribution } from "@/app/components/step-1-language-distribution";
import { ResourceRequirements} from "@/app/components/step-2-resource-requirements";
import { InstanceRecommendations} from "@/app/components/step-3-instance-recommendations";
import { } from "@/app/components/step-4-cloud-score-costs";
import { } from "@/app/components/step-5-anaylsis-details-llm-summary";
import Link from "next/link";
import { Button } from "@/app/components/ui/button";
import { LoadingComponent } from "../components/ui/loading";

export default function Results({
  searchParams,
}: {
  searchParams?: {
    repoUrl?: string;
    branchName?: string;
    directory?: string;
  };
}) {
  const encodedRepoUrl = encodeURIComponent(searchParams?.repoUrl || "");
  const encodedBranchName = encodeURIComponent(searchParams?.branchName || "");
  const encodedDirectory = encodeURIComponent(searchParams?.directory || "");
  const detailedPagePath =
    `/results-detail?repoUrl=${encodedRepoUrl}&branchName=${encodedBranchName}` +
    (encodedDirectory ? `&directory=${encodedDirectory}` : "");

  const repoUrl = searchParams?.repoUrl || "N/A";  // Default to "N/A" if undefined
  const branchName = searchParams?.branchName || "N/A";  // Default to "N/A" if undefined

    return (
      <div className="mx-auto max-w-7xl p-6 bg-background border">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">
          Analysis Results of branch
          <span style={{ color: 'hsl(var(--accent))' }}> {branchName} </span>
          in
          <span style={{ color: 'hsl(var(--accent))' }}> {repoUrl}</span>
        </CardTitle>
      </CardHeader>
      <div className="flex flex-wrap -mx-2">
        <div className="w-full md:w-1/2 px-2">
          <Suspense fallback={<LoadingComponent />}>
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center">Language Distribution</CardTitle>
              </CardHeader>
              <LanguageDistribution
                languages={{
                  JavaScript: 1500,
                  TypeScript: 800,
                  HTML: 400,
                  CSS: 200,
                  Python: 100,
                }}
              />
            </Card>
          </Suspense>
        </div>
        <div className="w-full md:w-1/2 px-2">
          <Suspense fallback={<LoadingComponent />}>
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center">Resource Requirements</CardTitle>
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
                <CardTitle className="text-xl font-bold text-center"> Instance Recommendations</CardTitle>
              </CardHeader>
              {/* <InstanceRecommendations
                repoUrl={searchParams?.repoUrl || ""}
                branchName={searchParams?.branchName || ""}
                directory={searchParams?.directory || ""}
              /> */}
            </Card>
          </Suspense>
        </div>
        <div className="w-full md:w-1/2 px-2 mt-5">
          <Suspense fallback={<LoadingComponent />}>
            <Card className="mb-4">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-center"> Cloud Score Costs</CardTitle>
              </CardHeader>
              {/* <CloudScoreCosts
                repoUrl={searchParams?.repoUrl || ""}
                branchName={searchParams?.branchName || ""}
                directory={searchParams?.directory || ""}
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
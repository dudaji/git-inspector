import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/app/components/ui/card";
import AnalysisResults from "@/app/components/analysis-result";
import { Suspense } from "react";
import { LanguageDistribution } from "@/app/components/step-1-language-distribution";
import Link from "next/link";
import { Button } from "@/app/components/ui/button";

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

  return (
    <Card className="mx-auto max-w-2xl p-6 bg-background border">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Analysis Results</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <Suspense
          fallback={
            <div className="flex flex-col items-center justify-center py-8 space-y-4">
              <div className="h-8 w-8 animate-spin" />
              <div className="text-muted-foreground">Loading...</div>
              <div className="text-sm text-muted-foreground">
                This may take a few seconds...
              </div>
            </div>
          }
        >
          <LanguageDistribution
            languages={{
              JavaScript: 1500,
              TypeScript: 800,
              HTML: 400,
              CSS: 200,
              Python: 100,
            }}
          />
          <AnalysisResults
            repoUrl={searchParams?.repoUrl}
            branchName={searchParams?.branchName}
            directory={searchParams?.directory}
          />
        </Suspense>
        <Link href={detailedPagePath}>
          <Button className="mt-6 w-full">Detailed Analysis</Button>
        </Link>
      </CardContent>
    </Card>
  );
}

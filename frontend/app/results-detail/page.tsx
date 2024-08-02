import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/app/components/ui/card";
import { Suspense } from "react";
import AnalysisResultsDetail from "../components/analysis-result-detail";

export default function ResultsDetail({
  searchParams,
}: {
  searchParams?: {
    repoUrl?: string;
    branchName?: string;
    directory?: string;
  };
}) {
  return (
    <Card className="mx-auto max-w-2xl p-6 bg-background border">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">
          Detailed Analysis Results
        </CardTitle>
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
          <AnalysisResultsDetail
            repoUrl={searchParams?.repoUrl}
            branchName={searchParams?.branchName}
            directory={searchParams?.directory}
          />
        </Suspense>
      </CardContent>
    </Card>
  );
}

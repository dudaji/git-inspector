import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import AnalysisResults from "@/components/analysis-result";

export default function Results({
  searchParams,
}: {
  searchParams?: {
    repoUrl?: string;
    branchName?: string;
  };
}) {
  const repoUrl = searchParams?.repoUrl || "";
  const branchName = searchParams?.branchName || "";
  return (
    <Card className="mx-auto max-w-md p-6 bg-background border">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Analysis Results</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <AnalysisResults repoUrl={repoUrl} branchName={branchName} />
      </CardContent>
    </Card>
  );
}

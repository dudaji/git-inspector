import { fetchAnalysisData } from "@/app/lib/fetch";

export default async function AnalysisResults({
  repoUrl,
  branchName,
  directory,
}: {
  repoUrl?: string;
  branchName?: string;
  directory?: string;
}) {
  const result = await fetchAnalysisData(repoUrl, branchName, directory);

  if (result?.message || result?.message != "") {
    return (
      <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
        {`ERROR: ${result.message}`}
      </div>
    );
  }

  if (Object.keys(result).length == 0) {
    return <p>No results available.</p>;
  }

  return (
    <div>
      <div>
        <h3 className="text-xl font-semibold">Predictions:</h3>
        <p>Power: {result?.power}</p>
        <p>Carbon: {result?.carbon}</p>
        <p>Cost: {result?.cost}</p>
      </div>
    </div>
  );
}

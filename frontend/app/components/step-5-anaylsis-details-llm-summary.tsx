import { fetchAnalysisData } from "@/app/lib/fetch";

export default async function AnalysisResultsDetail({
  repoUrl,
  branchName,
  directory,
}: {
  repoUrl?: string;
  branchName?: string;
  directory?: string;
}) {
  const result = await fetchAnalysisData(repoUrl, branchName, directory);

  if (result?.message) {
    return (
      <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
        {`ERROR: ${result.message}`}
      </div>
    );
  }

  if (Object.keys(result).length == 0) {
    return <p>No results available.</p>;
  }

  // TODO: Order by Scores.
  const cloudProviders = ["gcp", "aws", "azure"];
  const renderProviderData = (provider: string) => (
    <div key={provider} className="mb-8">
      <h4 className="text-lg font-semibold">{provider.toUpperCase()}</h4>
      <table className="table-auto w-full mb-4">
        <thead>
          <tr>
            <th className="px-4 py-2">Metric</th>
            <th className="px-4 py-2">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2">Instance Name</td>
            <td className="border px-4 py-2">
              {result[provider].instance.name}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">CPU</td>
            <td className="border px-4 py-2">
              {result[provider].instance.cpu}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Memory</td>
            <td className="border px-4 py-2">
              {result[provider].instance.ram} GB
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Storage</td>
            <td className="border px-4 py-2">
              {result[provider].instance.storage} GB
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">GPU</td>
            <td className="border px-4 py-2">
              {result[provider].instance.gpu || "None"}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Hourly Pricing</td>
            <td className="border px-4 py-2">
              ${result[provider].instance.cost_per_hour.toPrecision(3)}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Power Consumption (kWh)</td>
            <td className="border px-4 py-2">
              {result[provider].estimate.power_consumption}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2">Carbon Footprint (kg CO2)</td>
            <td className="border px-4 py-2">
              {result[provider].estimate.carbon_footprint}
            </td>
          </tr>
        </tbody>
      </table>
      <p>{result[provider].instance.description}</p>
    </div>
  );

  return (
    <div>
      {cloudProviders.map(renderProviderData)}
      <div className="mt-8 p-4 bg-green-100 border-l-4 border-green-500">
        <h4 className="text-lg font-semibold">Conclusion</h4>
        <p>{result.conclusion.instance.description}</p>
      </div>
    </div>
  );
}

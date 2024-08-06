import React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/app/components/ui/card";
import { RepoResult, CloudInstance } from "@/app/types/model";

interface ResourceRequirementsProps {
  data: RepoResult;
}

export function ResourceRequirements({ data }: ResourceRequirementsProps) {
  const getMinimumValues = () => {
    if (!data) return { minCpu: null, minMemory: null };

    const instances: CloudInstance[] = [
      data.gcp,
      data.aws,
      data.azure,
    ];

    const minCpu = Math.min(...instances.map(instance => instance.cpu));
    const minMemory = Math.min(...instances.map(instance => instance.ram));
    console.log("resource requirements parsing :", minCpu, minMemory);
    return { minCpu, minMemory };
  };

  const { minCpu, minMemory } = getMinimumValues();
  return (
    <Card className="flex flex-col bg-secondary-background h-full">
      <CardHeader className="items-center pb-0">
        <CardTitle>Minimum Resources to Run</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center justify-center h-full">
        <div className="flex items-center">
          <div className="text-4xl font-bold text-primary">
            {minCpu !== null ? minCpu : "N/A"}
          </div>
          <div className="text-4xl font-medium text-muted-foreground">CPU</div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-4xl font-bold text-primary">
            {minMemory !== null ? minMemory : "N/A"}
          </div>
          <div className="text-4xl font-medium text-muted-foreground">
            Gi Memory
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
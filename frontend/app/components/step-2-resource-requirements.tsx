"use client";

import React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/app/components/ui/card";
import { fetchResourceRequirements } from "@/app/lib/fetch";

export async function ResourceRequirements({ repoUrl }: { repoUrl: string }) {
  const requirements = await fetchResourceRequirements(repoUrl);
  return (
    <Card className="flex flex-col bg-secondary-background h-full">
      <CardHeader className="items-center pb-0">
        <CardTitle>CPU ,Memory</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center justify-center h-full">
        <div className="flex items-center space-x-2">
          <div className="text-4xl font-bold text-primary">
            {/* {requirements.cpu} */}
            2
          </div>
          <div className="text-4xl font-medium text-muted-foreground">CPU</div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-4xl font-bold text-primary">
            {/* {requirements.memory}
             */}
             4
          </div>
          <div className="text-4xl font-medium text-muted-foreground">Gi Memory</div>
        </div>
      </CardContent>
    </Card>
  );
}

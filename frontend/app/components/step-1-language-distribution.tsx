"use client";
// NOTE : Need to Render in Client Sides
import React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/app/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/app/components/ui/chart";
import { Label, PieChart, Pie } from "recharts";
import githubColors from 'github-colors';


interface LanguageDistributionProps {
  data: {
    languageRatio?: Record<string, number>;
  };
}

export function LanguageDistribution({ data }: LanguageDistributionProps) {
  // console.log("Render languageDistribution with fetched data: ", data);
  const languages = React.useMemo(() => data?.languageRatio || {}, [data]);
  
  const chartData = React.useMemo(
    () =>
      Object.entries(languages).map(([language, bytes]) => {
        const colorData = githubColors.get(language);
        console.log("colordata? ", colorData)
        return {
          language,
          value: bytes,
          fill: colorData?.color || "#808080", // 기본 색상 사용
        };
      }),
    [languages]
  );


  const chartConfig = {
    languages: {
      label: "Bytes",
    },
  };

  const totalLanguageBytes = React.useMemo(() => {
    return chartData.reduce((acc, curr) => acc + (curr.value as number), 0);
  }, [chartData]);

  return (
    <Card className="flex flex-col bg-secondary-background">
      <CardHeader className="items-center pb-0">
        <CardTitle>Programming Languages</CardTitle>
        <CardDescription>Byte Counts</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px]"
        >
          <PieChart>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={chartData}
              dataKey="value" // 변경된 부분
              nameKey="language"
              innerRadius={60}
              strokeWidth={5}
            >
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text
                        x={viewBox.cx}
                        y={viewBox.cy}
                        textAnchor="middle"
                        dominantBaseline="middle"
                      >
                        <tspan
                          x={viewBox.cx}
                          y={viewBox.cy}
                          className="fill-foreground text-2xl font-bold"
                        >
                          {totalLanguageBytes.toLocaleString()}
                        </tspan>
                        <tspan
                          x={viewBox.cx}
                          y={(viewBox.cy || 0) + 24}
                          className="fill-muted-foreground"
                        >
                          Total Bytes
                        </tspan>
                      </text>
                    );
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}

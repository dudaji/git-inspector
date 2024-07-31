/**
 * This code was generated by v0 by Vercel.
 * @see https://v0.dev/t/Y8Jlck6IDAX
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */

/** Add fonts into your Next.js project:

import { Inter } from 'next/font/google'

inter({
  subsets: ['latin'],
  display: 'swap',
})

To read more about using these font, please visit the Next.js documentation:
- App Directory: https://nextjs.org/docs/app/building-your-application/optimizing/fonts
- Pages Directory: https://nextjs.org/docs/pages/building-your-application/optimizing/fonts
**/
"use client";

import { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/app/components/ui/card";
import { Label } from "@/app/components/ui/label";
import { Input } from "@/app/components/ui/input";
import { Button } from "@/app/components/ui/button";
import { useRouter } from "next/navigation";
// import Link from "next/link";

export function GitRepoAnalyzer() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [repoUrl, setRepoUrl] = useState("");
  const [branchName, setBranchName] = useState("main");
  const [directory, setDirectory] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const encodedRepoUrl = encodeURIComponent(repoUrl);
      const encodedBranchName = encodeURIComponent(branchName);
      const encodedDirectory = encodeURIComponent(directory);
      const path =
        `/results?repoUrl=${encodedRepoUrl}&branchName=${encodedBranchName}` +
        (directory ? `&directory=${encodedDirectory}` : "");

      router.push(path);
      setLoading(false);
    } catch (err) {
      setLoading(false);
      if (err instanceof Error) {
        setError("Error: " + err.message);
      } else {
        setError("An unknown error occurred");
      }
    }
  };
  return (
    <Card className="mx-auto max-w-md p-6 bg-background border">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Git Repo Analyzer</CardTitle>
        <CardDescription className="text-muted-foreground">
          Enter a repository URL, branch name and code directory to analyze.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={handleSubmit}>
          <div className="space-y-2">
            <Label htmlFor="repo-url">Repository URL</Label>
            <Input
              id="repo-url"
              placeholder="https://github.com/user/repo.git"
              required
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
            />
          </div>
          <div className="space-y-2 mt-4">
            <Label htmlFor="branch-name">Branch Name</Label>
            <Input
              id="branch-name"
              placeholder="main"
              required
              value={branchName}
              onChange={(e) => setBranchName(e.target.value)}
            />
          </div>
          <div className="space-y-2 mt-4">
            <Label htmlFor="directory">Directory</Label>
            <Input
              id="directory"
              placeholder=""
              value={directory}
              onChange={(e) => setDirectory(e.target.value)}
            />
          </div>
          {loading ? (
            <div className="flex flex-col items-center justify-center py-8 space-y-4">
              <div className="h-8 w-8 animate-spin" />
              <div className="text-muted-foreground">Loading...</div>
              <div className="text-sm text-muted-foreground">
                This may take a few seconds...
              </div>
            </div>
          ) : (
            <Button type="submit" className="mt-6 w-full">
              Analyze Repository
            </Button>
          )}
          {error && (
            <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
              {error}
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}

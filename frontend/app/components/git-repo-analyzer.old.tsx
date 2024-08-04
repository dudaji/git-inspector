// /**
//  * This code was generated by v0 by Vercel.
//  * @see https://v0.dev/t/Y8Jlck6IDAX
//  * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
//  */

// /** Add fonts into your Next.js project:

// import { Inter } from 'next/font/google'

// inter({
//   subsets: ['latin'],
//   display: 'swap',
// })

// To read more about using these font, please visit the Next.js documentation:
// - App Directory: https://nextjs.org/docs/app/building-your-application/optimizing/fonts
// - Pages Directory: https://nextjs.org/docs/pages/building-your-application/optimizing/fonts
// **/
// "use client";

// import { useState } from "react";
// import {
//   Card,
//   CardHeader,
//   CardTitle,
//   CardDescription,
//   CardContent,
// } from "@/app/components/ui/card";
// import { Label } from "@/app/components/ui/label";
// import { Input } from "@/app/components/ui/input";
// import { Button } from "@/app/components/ui/button";
// import { useRouter } from "next/navigation";
// import { TypingText } from "./ui/typing";
// import Image from 'next/image';
// import Loading from '../../app/assets/images/loading-blue.gif'


// export function GitRepoAnalyzer() {
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);
//   const [repoUrl, setRepoUrl] = useState("");
//   const [branchName, setBranchName] = useState("");
//   const [directory, setDirectory] = useState("");
//   const router = useRouter();

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);
//     setError(null);

//     try {
//       const encodedRepoUrl = encodeURIComponent(repoUrl);
//       const encodedBranchName = encodeURIComponent(branchName);
//       const encodedDirectory = encodeURIComponent(directory);
//       const path =
//         `/results?repoUrl=${encodedRepoUrl}&branchName=${encodedBranchName}` +
//         (directory ? `&directory=${encodedDirectory}` : "");

//       setTimeout(() => {
//         router.push(path);
//         setLoading(false);
//       }, 1500); // 최소 1.5초 동안 로딩 상태 유지(개발용)
//     } catch (err) {
//       setLoading(false);
//       if (err instanceof Error) {
//         setError("Error: " + err.message);
//       } else {
//         setError("An unknown error occurred");
//       }
//     }
//   };

//   return (
//     <div className="relative mx-auto max-w-md p-[1.5px] rounded-full overflow-hidden">
//      <div className="animate-rotate absolute inset-0 h-full w-full rounded-full bg-[conic-gradient(#FFFFFF_30deg,transparent_1200deg)]"></div>
//       <Card className="relative p-6 bg-background rounded-full">
//         <CardHeader>
//           <CardTitle className="text-2xl font-bold">Git Watt</CardTitle>
//           <CardDescription className="text-muted-foreground">
//             Enter a Git Repo URL, Branch name to inspect
//           </CardDescription>
//         </CardHeader>
//         <CardContent className="space-y-4">
//           <form onSubmit={handleSubmit}>
//             <div className="space-y-2 mt-4">
//               <Label htmlFor="repo-url">
//                 Repository URL <span>*</span>
//               </Label>
//               <Input
//                 id="repo-url"
//                 placeholder="https://your-git-repository"
//                 required
//                 value={repoUrl}
//                 onChange={(e) => setRepoUrl(e.target.value)}
//                 />
//             </div>
//             <div className="space-y-2 mt-4">
//               <Label htmlFor="branch-name">
//                 Branch Name <span>*</span>
//               </Label>
//               <Input
//                 id="branch-name"
//                 placeholder="main"
//                 required
//                 value={branchName}
//                 onChange={(e) => setBranchName(e.target.value)}
//                 />
//             </div>
//             <div className="space-y-2 mt-4">
//                 <Label htmlFor="directory">
//                   Directory <span>(Optional)</span>
//                 </Label>
//               <Input
//                 id="directory"
//                 placeholder="Optional"
//                 value={directory}
//                 onChange={(e) => setDirectory(e.target.value)}
//                 />
//             </div>
//             {loading ? (
//               <div className="flex flex-col items-center justify-center py-8 space-y-4">
//                 <Image
//                   src={Loading}
//                   alt="Loading"
//                   width={180} // Provide width in pixels
//                   height={180} // Provide height in pixels
//                 />
//                 <div className="text-muted-foreground">
//                   <TypingText text="Analyzing repository with GEMINI API..." />
//                 </div>
//               </div>
//             ) : (
//               <div className="relative mt-6 w-full animate-pulse-border">
//                 <div className="absolute inset-0 animate-pulse-border rounded-lg"></div>
//                 <Button type="submit" className="relative w-full">
//                   Analyze Repository
//                 </Button>
//               </div>
//             )}
//             {error && (
//               <div className="mt-4 rounded-md bg-red-500/10 p-4 text-red-500">
//                 {error}
//               </div>
//             )}
//           </form>
//         </CardContent>
//       </Card>
//     </div>
//   );
// }
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Git Inspector - Optimize Cloud Deployment",
  description:
    "Analyze your Git repository to determine the most economical and eco-friendly cloud platform for deployment using Google Gemini",
  keywords: [
    "Google",
    "Firebase",
    "Gemini",
    "Cloud Platform",
    "Eco-friendly",
    "Cost Optimization",
    "Git Repository Analysis",
    "Sustainability",
    "Green Computing",
  ],
  openGraph: {
    title: "Git Inspector - Optimize Cloud Deployment",
    description:
      "Analyze your Git repository to determine the most economical and eco-friendly cloud platform for deployment using Google Gemini",
    url: "https://git-inspector-nextjs14--gpu-brokerage.us-central1.hosted.app/",
    images: [
      {
        url: "",
        width: 1200,
        height: 630,
        alt: "",
      },
    ],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex flex-col min-h-screen">
          <header className="bg-muted p-4">
            <nav className="container mx-auto flex items-center justify-between">
              <Link href="/" className="text-lg font-bold" prefetch={false}>
                Git Repo Analyzer
              </Link>
            </nav>
          </header>
          <main className="flex-1 py-12">{children}</main>
          <footer className="bg-muted p-4 text-center text-muted-foreground">
            <div className="container mx-auto">
              &copy; 2024 Git Repo Analyzer. All rights reserved.
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}

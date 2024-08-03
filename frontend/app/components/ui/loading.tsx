import Image from "next/image";
import { TypingText } from "@/app/components/ui/typing";
import Loading from "@/app/assets/images/loading.gif"; // 이미지 경로에 맞게 수정하세요

export function LoadingComponent() {
  return (
    <div className="flex flex-col items-center justify-center py-8 space-y-4">
      <Image
        src={Loading}
        alt="Loading"
        width={180} // Provide width in pixels
        height={180} // Provide height in pixels
      />
      <div className="text-muted-foreground">
        <TypingText text="Analyzing repository with GEMINI API..." />
      </div>
    </div>
  );
}

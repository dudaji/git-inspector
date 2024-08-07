declare module 'github-colors' {
    interface LanguageColor {
      color: string;
      url: string;
    }
  
    export default function colors(language: string): LanguageColor;
  }
  
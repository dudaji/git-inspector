declare module 'github-colors' {
  interface LanguageColor {
    color: string;
    url: string;
  }

  function get(language: string): LanguageColor;

  export = { get };
}

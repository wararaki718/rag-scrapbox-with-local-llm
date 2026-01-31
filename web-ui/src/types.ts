export interface SearchResult {
  text: string;
  title: string;
  url: string;
  score: number;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: SearchResult[];
}

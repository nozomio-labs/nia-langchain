import { getEnvironmentVariable } from "@langchain/core/utils/env";

const NIA_BASE_URL = "https://apigcp.trynia.ai/v2";

export interface NiaAPIWrapperParams {
  niaApiKey?: string;
  baseUrl?: string;
  timeout?: number;
}

function stripNulls(
  obj: Record<string, unknown>
): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value != null) {
      result[key] = value;
    }
  }
  return result;
}

export class NiaAPIWrapper {
  niaApiKey: string;

  baseUrl: string;

  timeout: number;

  constructor(params: NiaAPIWrapperParams = {}) {
    const apiKey =
      params.niaApiKey ?? getEnvironmentVariable("NIA_API_KEY");
    if (!apiKey) {
      throw new Error(
        "Nia API key must be provided via 'niaApiKey' parameter " +
          "or 'NIA_API_KEY' environment variable."
      );
    }
    this.niaApiKey = apiKey;
    const envUrl =
      typeof process !== "undefined"
        ? process.env?.NIA_API_URL
        : undefined;
    this.baseUrl = (params.baseUrl ?? envUrl ?? NIA_BASE_URL).replace(
      /\/$/,
      ""
    );
    this.timeout = params.timeout ?? 60_000;
  }

  private get headers(): Record<string, string> {
    return {
      Authorization: `Bearer ${this.niaApiKey}`,
      "Content-Type": "application/json",
      "User-Agent": "langchain-nia-js/0.1.0",
    };
  }

  async request(
    method: string,
    path: string,
    options?: {
      json?: Record<string, unknown>;
      params?: Record<string, unknown>;
    }
  ): Promise<unknown> {
    const url = new URL(`${this.baseUrl}${path}`);
    if (options?.params) {
      const cleaned = stripNulls(options.params);
      for (const [key, value] of Object.entries(cleaned)) {
        url.searchParams.set(key, String(value));
      }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url.toString(), {
        method,
        headers: this.headers,
        body: options?.json ? JSON.stringify(stripNulls(options.json)) : undefined,
        signal: controller.signal,
      });

      if (!response.ok) {
        const text = await response.text().catch(() => "");
        throw new Error(
          `Nia API error ${response.status}: ${text}`
        );
      }

      return await response.json();
    } finally {
      clearTimeout(timeoutId);
    }
  }

  // ── Search ──────────────────────────────────────────────────────────

  async searchQuery(params: {
    messages: Array<{ role: string; content: string }>;
    repositories?: string[];
    dataSources?: string[];
    slackWorkspaces?: string[];
    localFolders?: string[];
    fastMode?: boolean;
    includeSources?: boolean;
    maxTokens?: number;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      mode: "query",
      messages: params.messages,
      fast_mode: params.fastMode ?? true,
      include_sources: params.includeSources ?? true,
    };
    if (params.repositories) body.repositories = params.repositories;
    if (params.dataSources) body.data_sources = params.dataSources;
    if (params.slackWorkspaces)
      body.slack_workspaces = params.slackWorkspaces;
    if (params.localFolders) body.local_folders = params.localFolders;
    if (params.maxTokens != null) body.max_tokens = params.maxTokens;
    return this.request("POST", "/search", { json: body });
  }

  async searchWeb(params: {
    query: string;
    numResults?: number;
    category?: string;
    daysBack?: number;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      mode: "web",
      query: params.query,
      num_results: params.numResults ?? 5,
    };
    if (params.category) body.category = params.category;
    if (params.daysBack != null) body.days_back = params.daysBack;
    return this.request("POST", "/search", { json: body });
  }

  async searchDeep(params: {
    query: string;
    outputFormat?: string;
    verbose?: boolean;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      mode: "deep",
      query: params.query,
      verbose: params.verbose ?? false,
    };
    if (params.outputFormat) body.output_format = params.outputFormat;
    return this.request("POST", "/search", { json: body });
  }

  async searchUniversal(params: {
    query: string;
    topK?: number;
    includeRepos?: boolean;
    includeDocs?: boolean;
    compressOutput?: boolean;
    maxTokens?: number;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      mode: "universal",
      query: params.query,
      top_k: params.topK ?? 20,
      include_repos: params.includeRepos ?? true,
      include_docs: params.includeDocs ?? true,
      compress_output: params.compressOutput ?? false,
    };
    if (params.maxTokens != null) body.max_tokens = params.maxTokens;
    return this.request("POST", "/search", { json: body });
  }

  // ── Advisor ─────────────────────────────────────────────────────────

  async advisor(params: {
    query: string;
    codebase: string;
    searchScope?: string[];
    outputFormat?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      query: params.query,
      codebase: params.codebase,
    };
    if (params.searchScope) body.search_scope = params.searchScope;
    if (params.outputFormat) body.output_format = params.outputFormat;
    return this.request("POST", "/advisor", { json: body });
  }

  // ── Sources ─────────────────────────────────────────────────────────

  async sourceCreate(params: {
    url?: string;
    type?: string;
    displayName?: string;
    branch?: string;
    urlPatterns?: string[];
    excludePatterns?: string[];
    checkLlmsTxt?: boolean;
    repository?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {};
    if (params.url) body.url = params.url;
    if (params.type) body.type = params.type;
    if (params.displayName) body.display_name = params.displayName;
    if (params.branch) body.branch = params.branch;
    if (params.urlPatterns) body.url_patterns = params.urlPatterns;
    if (params.excludePatterns)
      body.exclude_patterns = params.excludePatterns;
    if (params.checkLlmsTxt != null)
      body.check_llms_txt = params.checkLlmsTxt;
    if (params.repository) body.repository = params.repository;
    return this.request("POST", "/sources", { json: body });
  }

  async sourcesList(params?: {
    type?: string;
    query?: string;
    status?: string;
    limit?: number;
    offset?: number;
  }): Promise<unknown> {
    const p: Record<string, unknown> = {
      limit: params?.limit ?? 20,
      offset: params?.offset ?? 0,
    };
    if (params?.type) p.type = params.type;
    if (params?.query) p.query = params.query;
    if (params?.status) p.status = params.status;
    return this.request("GET", "/sources", { params: p });
  }

  async sourceSubscribe(params: {
    url: string;
    sourceType?: string;
    ref?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = { url: params.url };
    if (params.sourceType) body.source_type = params.sourceType;
    if (params.ref) body.ref = params.ref;
    return this.request("POST", "/sources/subscribe", { json: body });
  }

  async sourceSync(sourceId: string): Promise<unknown> {
    return this.request("POST", `/sources/${sourceId}/sync`);
  }

  async sourceContent(params: {
    sourceId: string;
    path?: string;
    url?: string;
    branch?: string;
    page?: number;
    lineStart?: number;
    lineEnd?: number;
  }): Promise<unknown> {
    const p: Record<string, unknown> = {};
    if (params.path) p.path = params.path;
    if (params.url) p.url = params.url;
    if (params.branch) p.branch = params.branch;
    if (params.page != null) p.page = params.page;
    if (params.lineStart != null) p.line_start = params.lineStart;
    if (params.lineEnd != null) p.line_end = params.lineEnd;
    return this.request("GET", `/sources/${params.sourceId}/content`, {
      params: p,
    });
  }

  async sourceGrep(params: {
    sourceId: string;
    pattern: string;
    fileExtensions?: string[];
    contextLines?: number;
  }): Promise<unknown> {
    const body: Record<string, unknown> = { pattern: params.pattern };
    if (params.fileExtensions)
      body.file_extensions = params.fileExtensions;
    if (params.contextLines != null)
      body.context_lines = params.contextLines;
    return this.request("POST", `/sources/${params.sourceId}/grep`, {
      json: body,
    });
  }

  async sourceTree(params: {
    sourceId: string;
    branch?: string;
    maxDepth?: number;
  }): Promise<unknown> {
    const p: Record<string, unknown> = {};
    if (params.branch) p.branch = params.branch;
    if (params.maxDepth != null) p.max_depth = params.maxDepth;
    return this.request("GET", `/sources/${params.sourceId}/tree`, {
      params: p,
    });
  }

  // ── GitHub ──────────────────────────────────────────────────────────

  async githubSearch(params: {
    query: string;
    repository: string;
    language?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      query: params.query,
      repository: params.repository,
    };
    if (params.language) body.language = params.language;
    return this.request("POST", "/github/search", { json: body });
  }

  async githubRead(params: {
    repository: string;
    path: string;
    ref?: string;
    startLine?: number;
    endLine?: number;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      repository: params.repository,
      path: params.path,
    };
    if (params.ref) body.ref = params.ref;
    if (params.startLine != null) body.start_line = params.startLine;
    if (params.endLine != null) body.end_line = params.endLine;
    return this.request("POST", "/github/read", { json: body });
  }

  async githubGlob(params: {
    repository: string;
    pattern: string;
    ref?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      repository: params.repository,
      pattern: params.pattern,
    };
    if (params.ref) body.ref = params.ref;
    return this.request("POST", "/github/glob", { json: body });
  }

  async githubTree(params: {
    owner: string;
    repo: string;
    ref?: string;
    path?: string;
  }): Promise<unknown> {
    const p: Record<string, unknown> = {};
    if (params.ref) p.ref = params.ref;
    if (params.path) p.path = params.path;
    return this.request(
      "GET",
      `/github/tree/${params.owner}/${params.repo}`,
      { params: p }
    );
  }

  // ── Contexts ────────────────────────────────────────────────────────

  async contextSave(params: {
    title: string;
    summary: string;
    content: string;
    agentSource?: string;
    tags?: string[];
    memoryType?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      title: params.title,
      summary: params.summary,
      content: params.content,
    };
    if (params.agentSource) body.agent_source = params.agentSource;
    if (params.tags) body.tags = params.tags;
    if (params.memoryType) body.memory_type = params.memoryType;
    return this.request("POST", "/contexts", { json: body });
  }

  async contextSearch(params: {
    q: string;
    limit?: number;
    includeHighlights?: boolean;
  }): Promise<unknown> {
    const p: Record<string, unknown> = {
      q: params.q,
      limit: params.limit ?? 20,
      include_highlights: params.includeHighlights ?? false,
    };
    return this.request("GET", "/contexts/semantic-search", {
      params: p,
    });
  }

  // ── Dependencies ────────────────────────────────────────────────────

  async dependencySubscribe(params: {
    manifestContent: string;
    manifestType?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      manifest_content: params.manifestContent,
    };
    if (params.manifestType) body.manifest_type = params.manifestType;
    return this.request("POST", "/dependencies/subscribe", {
      json: body,
    });
  }

  async dependencyAnalyze(params: {
    manifestContent: string;
    manifestType?: string;
  }): Promise<unknown> {
    const body: Record<string, unknown> = {
      manifest_content: params.manifestContent,
    };
    if (params.manifestType) body.manifest_type = params.manifestType;
    return this.request("POST", "/dependencies/analyze", { json: body });
  }
}

import { z } from "zod";
import { CallbackManagerForToolRun } from "@langchain/core/callbacks/manager";
import { StructuredTool, ToolParams } from "@langchain/core/tools";
import { NiaAPIWrapper, type NiaAPIWrapperParams } from "./utils.js";

// ── Shared base ──────────────────────────────────────────────────────

export interface NiaToolFields extends ToolParams {
  niaApiKey?: string;
  apiWrapper?: NiaAPIWrapper;
}

function resolveWrapper(params: NiaToolFields): NiaAPIWrapper {
  if (params.apiWrapper) return params.apiWrapper;
  const wrapperParams: NiaAPIWrapperParams = {};
  if (params.niaApiKey) wrapperParams.niaApiKey = params.niaApiKey;
  return new NiaAPIWrapper(wrapperParams);
}

// ── Search tools ─────────────────────────────────────────────────────

const niaSearchSchema = z.object({
  query: z.string().describe("Natural language search query"),
  repositories: z
    .array(z.string())
    .optional()
    .describe("Repository slugs (owner/repo) to search within"),
  dataSources: z
    .array(z.string())
    .optional()
    .describe("Data source IDs or display names to search"),
  slackWorkspaces: z
    .array(z.string())
    .optional()
    .describe("Slack workspace IDs to include in search"),
  localFolders: z
    .array(z.string())
    .optional()
    .describe("Local folder IDs to include in search"),
});

export class NiaSearch extends StructuredTool<typeof niaSearchSchema> {
  static lc_name() {
    return "NiaSearch";
  }

  name = "nia_search";

  description =
    "Search across code repositories, documentation, datasets, and " +
    "other sources indexed in Nia using natural language queries.";

  schema = niaSearchSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaSearchSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.searchQuery({
        messages: [{ role: "user", content: input.query }],
        repositories: input.repositories,
        dataSources: input.dataSources,
        slackWorkspaces: input.slackWorkspaces,
        localFolders: input.localFolders,
      });
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaWebSearchSchema = z.object({
  query: z.string().describe("Web search query"),
  numResults: z
    .number()
    .optional()
    .default(5)
    .describe("Number of results to return"),
  category: z
    .string()
    .optional()
    .describe(
      "Category filter: github, company, research, news, tweet, pdf, blog"
    ),
  daysBack: z
    .number()
    .optional()
    .describe("Only include results from the last N days"),
});

export class NiaWebSearch extends StructuredTool<typeof niaWebSearchSchema> {
  static lc_name() {
    return "NiaWebSearch";
  }

  name = "nia_web_search";

  description =
    "Search the web for real-time information with optional " +
    "category filtering and date range.";

  schema = niaWebSearchSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaWebSearchSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.searchWeb(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaDeepResearchSchema = z.object({
  query: z.string().describe("Research query or question"),
  outputFormat: z
    .string()
    .optional()
    .describe("Output format for the research results"),
  verbose: z
    .boolean()
    .optional()
    .default(false)
    .describe("Enable verbose output with intermediate steps"),
});

export class NiaDeepResearch extends StructuredTool<
  typeof niaDeepResearchSchema
> {
  static lc_name() {
    return "NiaDeepResearch";
  }

  name = "nia_deep_research";

  description =
    "Perform multi-step comprehensive research on a topic across " +
    "all indexed sources.";

  schema = niaDeepResearchSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaDeepResearchSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.searchDeep(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaUniversalSearchSchema = z.object({
  query: z.string().describe("Search query"),
  topK: z
    .number()
    .optional()
    .default(20)
    .describe("Maximum number of results to return"),
  includeRepos: z
    .boolean()
    .optional()
    .default(true)
    .describe("Include repository results"),
  includeDocs: z
    .boolean()
    .optional()
    .default(true)
    .describe("Include documentation results"),
  compressOutput: z
    .boolean()
    .optional()
    .default(false)
    .describe("Compress output to reduce token usage"),
});

export class NiaUniversalSearch extends StructuredTool<
  typeof niaUniversalSearchSchema
> {
  static lc_name() {
    return "NiaUniversalSearch";
  }

  name = "nia_universal_search";

  description =
    "Search all indexed sources simultaneously — repos, docs, " +
    "datasets, papers, and more.";

  schema = niaUniversalSearchSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaUniversalSearchSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.searchUniversal(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaAdvisorSchema = z.object({
  query: z.string().describe("Question or analysis request about the code"),
  codebase: z.string().describe("Code content to analyze"),
  searchScope: z
    .array(z.string())
    .optional()
    .describe("Source IDs to limit the advisory search scope"),
  outputFormat: z
    .string()
    .optional()
    .describe("Output format: explanation, checklist, diff, structured"),
});

export class NiaAdvisor extends StructuredTool<typeof niaAdvisorSchema> {
  static lc_name() {
    return "NiaAdvisor";
  }

  name = "nia_advisor";

  description =
    "Analyze code against indexed documentation to get " +
    "tailored recommendations and insights.";

  schema = niaAdvisorSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaAdvisorSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.advisor(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

// ── Source management tools ──────────────────────────────────────────

const niaIndexSchema = z.object({
  url: z.string().describe("URL of the source to index"),
  type: z
    .string()
    .optional()
    .describe(
      "Source type: repository, documentation, research_paper, huggingface_dataset"
    ),
  displayName: z.string().optional().describe("Display name for the source"),
  branch: z.string().optional().describe("Branch name for repositories"),
  urlPatterns: z
    .array(z.string())
    .optional()
    .describe("URL patterns to include when indexing docs"),
  excludePatterns: z
    .array(z.string())
    .optional()
    .describe("URL patterns to exclude when indexing docs"),
  checkLlmsTxt: z
    .boolean()
    .optional()
    .describe("Check for llms.txt at the domain root"),
});

export class NiaIndex extends StructuredTool<typeof niaIndexSchema> {
  static lc_name() {
    return "NiaIndex";
  }

  name = "nia_index";

  description =
    "Index a new source — repository, documentation site, paper, " +
    "or dataset — into Nia for searching and exploration.";

  schema = niaIndexSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaIndexSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourceCreate(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaSourceListSchema = z.object({
  type: z
    .string()
    .optional()
    .describe("Filter by source type: repository, documentation, etc."),
  query: z.string().optional().describe("Search query to filter sources"),
  status: z
    .string()
    .optional()
    .describe("Filter by status: indexed, pending, failed"),
  limit: z
    .number()
    .optional()
    .default(20)
    .describe("Maximum number of results"),
});

export class NiaSourceList extends StructuredTool<
  typeof niaSourceListSchema
> {
  static lc_name() {
    return "NiaSourceList";
  }

  name = "nia_source_list";

  description = "List indexed sources with optional filtering.";

  schema = niaSourceListSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaSourceListSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourcesList(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaSourceSubscribeSchema = z.object({
  url: z.string().describe("URL of the public source to subscribe to"),
  sourceType: z.string().optional().describe("Source type hint"),
  ref: z.string().optional().describe("Git ref for repositories"),
});

export class NiaSourceSubscribe extends StructuredTool<
  typeof niaSourceSubscribeSchema
> {
  static lc_name() {
    return "NiaSourceSubscribe";
  }

  name = "nia_source_subscribe";

  description = "Subscribe to a pre-indexed public source.";

  schema = niaSourceSubscribeSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaSourceSubscribeSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourceSubscribe(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaSourceSyncSchema = z.object({
  sourceId: z.string().describe("ID of the source to re-sync"),
});

export class NiaSourceSync extends StructuredTool<
  typeof niaSourceSyncSchema
> {
  static lc_name() {
    return "NiaSourceSync";
  }

  name = "nia_source_sync";

  description = "Re-sync an indexed source to pull latest changes.";

  schema = niaSourceSyncSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaSourceSyncSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourceSync(input.sourceId);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaReadSchema = z.object({
  sourceId: z.string().describe("ID of the indexed source"),
  path: z.string().optional().describe("File path within the source"),
  url: z.string().optional().describe("URL of the page to read"),
  branch: z.string().optional().describe("Branch for repository sources"),
  page: z.number().optional().describe("Page number for paginated sources"),
  lineStart: z.number().optional().describe("Starting line number"),
  lineEnd: z.number().optional().describe("Ending line number"),
});

export class NiaRead extends StructuredTool<typeof niaReadSchema> {
  static lc_name() {
    return "NiaRead";
  }

  name = "nia_read";

  description =
    "Read a file or page from an indexed source with optional line ranges.";

  schema = niaReadSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaReadSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourceContent(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaGrepSchema = z.object({
  sourceId: z.string().describe("ID of the indexed source to search"),
  pattern: z.string().describe("Regex pattern to search for"),
  fileExtensions: z
    .array(z.string())
    .optional()
    .describe("File extensions to filter (e.g. ['py', 'ts'])"),
  contextLines: z
    .number()
    .optional()
    .describe("Number of context lines around matches"),
});

export class NiaGrep extends StructuredTool<typeof niaGrepSchema> {
  static lc_name() {
    return "NiaGrep";
  }

  name = "nia_grep";

  description =
    "Search for a regex pattern within an indexed source's files.";

  schema = niaGrepSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaGrepSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourceGrep(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaExploreSchema = z.object({
  sourceId: z.string().describe("ID of the indexed source"),
  branch: z.string().optional().describe("Branch for repository sources"),
  maxDepth: z
    .number()
    .optional()
    .describe("Maximum depth of the file tree"),
});

export class NiaExplore extends StructuredTool<typeof niaExploreSchema> {
  static lc_name() {
    return "NiaExplore";
  }

  name = "nia_explore";

  description =
    "Browse the file tree structure of an indexed source.";

  schema = niaExploreSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaExploreSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.sourceTree(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

// ── GitHub tools ─────────────────────────────────────────────────────

const niaGitHubSearchSchema = z.object({
  query: z.string().describe("Code search query"),
  repository: z
    .string()
    .describe("GitHub repository in 'owner/repo' format"),
  language: z.string().optional().describe("Programming language filter"),
});

export class NiaGitHubSearch extends StructuredTool<
  typeof niaGitHubSearchSchema
> {
  static lc_name() {
    return "NiaGitHubSearch";
  }

  name = "nia_github_search";

  description =
    "Search code in any GitHub repository using GitHub Code Search.";

  schema = niaGitHubSearchSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaGitHubSearchSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.githubSearch(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaGitHubReadSchema = z.object({
  repository: z
    .string()
    .describe("GitHub repository in 'owner/repo' format"),
  path: z.string().describe("File path within the repository"),
  ref: z.string().optional().describe("Branch, tag, or commit SHA"),
  startLine: z.number().optional().describe("Starting line number"),
  endLine: z.number().optional().describe("Ending line number"),
});

export class NiaGitHubRead extends StructuredTool<
  typeof niaGitHubReadSchema
> {
  static lc_name() {
    return "NiaGitHubRead";
  }

  name = "nia_github_read";

  description =
    "Read a file from any GitHub repository with optional line ranges.";

  schema = niaGitHubReadSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaGitHubReadSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.githubRead(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaGitHubGlobSchema = z.object({
  repository: z
    .string()
    .describe("GitHub repository in 'owner/repo' format"),
  pattern: z
    .string()
    .describe("Glob pattern to match files, e.g. '**/*.ts'"),
  ref: z.string().optional().describe("Branch, tag, or commit SHA"),
});

export class NiaGitHubGlob extends StructuredTool<
  typeof niaGitHubGlobSchema
> {
  static lc_name() {
    return "NiaGitHubGlob";
  }

  name = "nia_github_glob";

  description =
    "Find files matching a glob pattern in any GitHub repository.";

  schema = niaGitHubGlobSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaGitHubGlobSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.githubGlob(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaGitHubTreeSchema = z.object({
  owner: z.string().describe("GitHub repository owner"),
  repo: z.string().describe("GitHub repository name"),
  ref: z.string().optional().describe("Branch, tag, or commit SHA"),
  path: z.string().optional().describe("Subdirectory path to list"),
});

export class NiaGitHubTree extends StructuredTool<
  typeof niaGitHubTreeSchema
> {
  static lc_name() {
    return "NiaGitHubTree";
  }

  name = "nia_github_tree";

  description =
    "Browse the file tree structure of any GitHub repository.";

  schema = niaGitHubTreeSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaGitHubTreeSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.githubTree(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

// ── Context tools ────────────────────────────────────────────────────

const niaContextSaveSchema = z.object({
  title: z.string().describe("Short title for the saved context"),
  summary: z.string().describe("Brief summary of the context"),
  content: z.string().describe("Full content to save"),
  agentSource: z
    .string()
    .optional()
    .describe("Identifier of the agent saving this context"),
  tags: z.array(z.string()).optional().describe("Tags for categorization"),
  memoryType: z
    .string()
    .optional()
    .describe(
      "Memory type: scratchpad, episodic, fact, or procedural"
    ),
});

export class NiaContextSave extends StructuredTool<
  typeof niaContextSaveSchema
> {
  static lc_name() {
    return "NiaContextSave";
  }

  name = "nia_context_save";

  description =
    "Save conversation context for cross-agent knowledge sharing.";

  schema = niaContextSaveSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaContextSaveSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.contextSave(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaContextSearchSchema = z.object({
  q: z.string().describe("Semantic search query"),
  limit: z
    .number()
    .optional()
    .default(20)
    .describe("Maximum number of results"),
  includeHighlights: z
    .boolean()
    .optional()
    .default(false)
    .describe("Include highlighted matching excerpts"),
});

export class NiaContextSearch extends StructuredTool<
  typeof niaContextSearchSchema
> {
  static lc_name() {
    return "NiaContextSearch";
  }

  name = "nia_context_search";

  description =
    "Semantic search over previously saved contexts.";

  schema = niaContextSearchSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaContextSearchSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.contextSearch(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

// ── Dependency tools ─────────────────────────────────────────────────

const niaDependencySubscribeSchema = z.object({
  manifestContent: z
    .string()
    .describe("Full content of the package manifest file"),
  manifestType: z
    .string()
    .optional()
    .describe(
      "Manifest type: package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod"
    ),
});

export class NiaDependencySubscribe extends StructuredTool<
  typeof niaDependencySubscribeSchema
> {
  static lc_name() {
    return "NiaDependencySubscribe";
  }

  name = "nia_dependency_subscribe";

  description =
    "Auto-subscribe to docs for all dependencies in a manifest.";

  schema = niaDependencySubscribeSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaDependencySubscribeSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.dependencySubscribe(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

const niaDependencyAnalyzeSchema = z.object({
  manifestContent: z
    .string()
    .describe("Full content of the package manifest file"),
  manifestType: z
    .string()
    .optional()
    .describe(
      "Manifest type: package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod"
    ),
});

export class NiaDependencyAnalyze extends StructuredTool<
  typeof niaDependencyAnalyzeSchema
> {
  static lc_name() {
    return "NiaDependencyAnalyze";
  }

  name = "nia_dependency_analyze";

  description =
    "Analyze a manifest to preview what dependencies would be indexed.";

  schema = niaDependencyAnalyzeSchema;

  apiWrapper: NiaAPIWrapper;

  constructor(params: NiaToolFields = {}) {
    super(params);
    this.apiWrapper = resolveWrapper(params);
  }

  async _call(
    input: z.output<typeof niaDependencyAnalyzeSchema>,
    _runManager?: CallbackManagerForToolRun
  ): Promise<string> {
    try {
      const result = await this.apiWrapper.dependencyAnalyze(input);
      return JSON.stringify(result);
    } catch (e) {
      return JSON.stringify({ error: String(e) });
    }
  }
}

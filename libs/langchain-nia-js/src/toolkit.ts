import { StructuredTool } from "@langchain/core/tools";
import { NiaAPIWrapper, type NiaAPIWrapperParams } from "./utils.js";
import {
  NiaSearch,
  NiaWebSearch,
  NiaDeepResearch,
  NiaUniversalSearch,
  NiaAdvisor,
  NiaIndex,
  NiaSourceList,
  NiaSourceSubscribe,
  NiaSourceSync,
  NiaRead,
  NiaGrep,
  NiaExplore,
  NiaGitHubSearch,
  NiaGitHubRead,
  NiaGitHubGlob,
  NiaGitHubTree,
  NiaContextSave,
  NiaContextSearch,
  NiaDependencySubscribe,
  NiaDependencyAnalyze,
} from "./tools.js";

export interface NiaToolkitParams extends NiaAPIWrapperParams {
  apiWrapper?: NiaAPIWrapper;
  includeSearch?: boolean;
  includeSources?: boolean;
  includeGithub?: boolean;
  includeContexts?: boolean;
  includeDependencies?: boolean;
}

export class NiaToolkit {
  apiWrapper: NiaAPIWrapper;

  includeSearch: boolean;

  includeSources: boolean;

  includeGithub: boolean;

  includeContexts: boolean;

  includeDependencies: boolean;

  constructor(params: NiaToolkitParams = {}) {
    this.apiWrapper =
      params.apiWrapper ?? new NiaAPIWrapper(params);
    this.includeSearch = params.includeSearch ?? true;
    this.includeSources = params.includeSources ?? true;
    this.includeGithub = params.includeGithub ?? true;
    this.includeContexts = params.includeContexts ?? true;
    this.includeDependencies = params.includeDependencies ?? true;
  }

  getTools(): StructuredTool[] {
    const tools: StructuredTool[] = [];
    const w = { apiWrapper: this.apiWrapper };

    if (this.includeSearch) {
      tools.push(
        new NiaSearch(w),
        new NiaWebSearch(w),
        new NiaDeepResearch(w),
        new NiaUniversalSearch(w),
        new NiaAdvisor(w)
      );
    }

    if (this.includeSources) {
      tools.push(
        new NiaIndex(w),
        new NiaSourceList(w),
        new NiaSourceSubscribe(w),
        new NiaSourceSync(w),
        new NiaRead(w),
        new NiaGrep(w),
        new NiaExplore(w)
      );
    }

    if (this.includeGithub) {
      tools.push(
        new NiaGitHubSearch(w),
        new NiaGitHubRead(w),
        new NiaGitHubGlob(w),
        new NiaGitHubTree(w)
      );
    }

    if (this.includeContexts) {
      tools.push(new NiaContextSave(w), new NiaContextSearch(w));
    }

    if (this.includeDependencies) {
      tools.push(
        new NiaDependencySubscribe(w),
        new NiaDependencyAnalyze(w)
      );
    }

    return tools;
  }
}

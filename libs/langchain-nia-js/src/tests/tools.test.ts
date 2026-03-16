import { test, expect, vi, describe, beforeEach } from "vitest";
import { NiaAPIWrapper } from "../utils.js";
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
} from "../tools.js";
import { NiaToolkit } from "../toolkit.js";

class TestAPIWrapper extends NiaAPIWrapper {
  constructor() {
    super({ niaApiKey: "nk_test_key" });
  }

  override async request(): Promise<unknown> {
    return { result: "mocked" };
  }
}

function makeWrapper(): TestAPIWrapper {
  return new TestAPIWrapper();
}

describe("NiaSearch", () => {
  test("has correct name and description", () => {
    const tool = new NiaSearch({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_search");
    expect(tool.description).toContain("Search across");
  });

  test("has valid schema", () => {
    const tool = new NiaSearch({ apiWrapper: makeWrapper() });
    expect(tool.schema).toBeDefined();
  });

  test("invokes successfully", async () => {
    const wrapper = makeWrapper();
    wrapper.request = vi.fn().mockResolvedValue({ content: "result" });
    const tool = new NiaSearch({ apiWrapper: wrapper });
    const result = await tool.invoke({ query: "test query" });
    expect(result).toContain("result");
  });

  test("handles errors", async () => {
    const wrapper = makeWrapper();
    wrapper.request = vi
      .fn()
      .mockRejectedValue(new Error("API error"));
    const tool = new NiaSearch({ apiWrapper: wrapper });
    const result = await tool.invoke({ query: "test" });
    expect(result).toContain("error");
  });
});

describe("NiaWebSearch", () => {
  test("has correct name", () => {
    const tool = new NiaWebSearch({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_web_search");
  });

  test("invokes successfully", async () => {
    const wrapper = makeWrapper();
    wrapper.request = vi.fn().mockResolvedValue({ results: [] });
    const tool = new NiaWebSearch({ apiWrapper: wrapper });
    const result = await tool.invoke({ query: "test" });
    expect(result).toContain("results");
  });
});

describe("NiaDeepResearch", () => {
  test("has correct name", () => {
    const tool = new NiaDeepResearch({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_deep_research");
  });
});

describe("NiaUniversalSearch", () => {
  test("has correct name", () => {
    const tool = new NiaUniversalSearch({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_universal_search");
  });
});

describe("NiaAdvisor", () => {
  test("has correct name", () => {
    const tool = new NiaAdvisor({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_advisor");
  });
});

describe("NiaIndex", () => {
  test("has correct name", () => {
    const tool = new NiaIndex({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_index");
  });
});

describe("NiaSourceList", () => {
  test("has correct name", () => {
    const tool = new NiaSourceList({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_source_list");
  });
});

describe("NiaSourceSubscribe", () => {
  test("has correct name", () => {
    const tool = new NiaSourceSubscribe({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_source_subscribe");
  });
});

describe("NiaSourceSync", () => {
  test("has correct name", () => {
    const tool = new NiaSourceSync({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_source_sync");
  });
});

describe("NiaRead", () => {
  test("has correct name", () => {
    const tool = new NiaRead({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_read");
  });
});

describe("NiaGrep", () => {
  test("has correct name", () => {
    const tool = new NiaGrep({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_grep");
  });
});

describe("NiaExplore", () => {
  test("has correct name", () => {
    const tool = new NiaExplore({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_explore");
  });
});

describe("NiaGitHubSearch", () => {
  test("has correct name", () => {
    const tool = new NiaGitHubSearch({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_github_search");
  });
});

describe("NiaGitHubRead", () => {
  test("has correct name", () => {
    const tool = new NiaGitHubRead({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_github_read");
  });
});

describe("NiaGitHubGlob", () => {
  test("has correct name", () => {
    const tool = new NiaGitHubGlob({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_github_glob");
  });
});

describe("NiaGitHubTree", () => {
  test("has correct name", () => {
    const tool = new NiaGitHubTree({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_github_tree");
  });
});

describe("NiaContextSave", () => {
  test("has correct name", () => {
    const tool = new NiaContextSave({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_context_save");
  });
});

describe("NiaContextSearch", () => {
  test("has correct name", () => {
    const tool = new NiaContextSearch({ apiWrapper: makeWrapper() });
    expect(tool.name).toBe("nia_context_search");
  });
});

describe("NiaDependencySubscribe", () => {
  test("has correct name", () => {
    const tool = new NiaDependencySubscribe({
      apiWrapper: makeWrapper(),
    });
    expect(tool.name).toBe("nia_dependency_subscribe");
  });
});

describe("NiaDependencyAnalyze", () => {
  test("has correct name", () => {
    const tool = new NiaDependencyAnalyze({
      apiWrapper: makeWrapper(),
    });
    expect(tool.name).toBe("nia_dependency_analyze");
  });
});

describe("NiaToolkit", () => {
  test("returns all 20 tools by default", () => {
    const toolkit = new NiaToolkit({ niaApiKey: "nk_test" });
    const tools = toolkit.getTools();
    expect(tools).toHaveLength(20);
  });

  test("respects include flags", () => {
    const toolkit = new NiaToolkit({
      niaApiKey: "nk_test",
      includeSearch: true,
      includeSources: false,
      includeGithub: false,
      includeContexts: false,
      includeDependencies: false,
    });
    const tools = toolkit.getTools();
    expect(tools).toHaveLength(5);
    expect(tools.map((t) => t.name)).toContain("nia_search");
  });

  test("shares a single API wrapper", () => {
    const wrapper = makeWrapper();
    const toolkit = new NiaToolkit({ apiWrapper: wrapper });
    const tools = toolkit.getTools();
    for (const tool of tools) {
      expect((tool as NiaSearch).apiWrapper).toBe(wrapper);
    }
  });
});

describe("NiaAPIWrapper", () => {
  test("throws without API key", () => {
    const original = process.env.NIA_API_KEY;
    delete process.env.NIA_API_KEY;
    try {
      expect(() => new NiaAPIWrapper()).toThrow("Nia API key");
    } finally {
      if (original) process.env.NIA_API_KEY = original;
    }
  });

  test("accepts key via constructor", () => {
    const wrapper = new NiaAPIWrapper({ niaApiKey: "nk_test" });
    expect(wrapper.niaApiKey).toBe("nk_test");
  });
});

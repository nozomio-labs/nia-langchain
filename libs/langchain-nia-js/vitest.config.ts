import { configDefaults, defineConfig } from "vitest/config";

export default defineConfig((env) => {
  if (env.mode === "int") {
    return {
      test: {
        environment: "node",
        testTimeout: 60_000,
        exclude: configDefaults.exclude,
        include: ["**/*.int.test.ts"],
        setupFiles: ["dotenv/config"],
      },
    };
  }

  return {
    test: {
      environment: "node",
      testTimeout: 30_000,
      exclude: ["**/*.int.test.ts", ...configDefaults.exclude],
    },
  };
});

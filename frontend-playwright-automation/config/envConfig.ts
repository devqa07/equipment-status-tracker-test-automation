export interface EnvironmentConfig {
  baseUrl: string;
  apiUrl: string;
  timeout: number;
  retries: number;
  headless: boolean;
  slowMo: number;
}

export const environments: Record<string, EnvironmentConfig> = {
  qa: {
    baseUrl: 'https://qa-assignment-omega.vercel.app',
    apiUrl: 'https://qa-assignment-omega.vercel.app/api',
    timeout: 30000,
    retries: 2,
    headless: false,
    slowMo: 1000,
  },
  staging: {
    baseUrl: 'https://staging-assignment-omega.vercel.app',
    apiUrl: 'https://staging-assignment-omega.vercel.app/api',
    timeout: 30000,
    retries: 1,
    headless: true,
    slowMo: 500,
  },
  production: {
    baseUrl: 'https://assignment-omega.vercel.app',
    apiUrl: 'https://assignment-omega.vercel.app/api',
    timeout: 60000,
    retries: 0,
    headless: true,
    slowMo: 0,
  },
};

export const getEnvironment = (): EnvironmentConfig => {
  const env = process.env.TEST_ENV || 'qa';
  return environments[env] || environments.qa;
};

export const currentEnv = getEnvironment(); 
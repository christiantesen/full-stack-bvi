const isDevelopment = import.meta.env.DEV;

export const logger = {
  info: (message: string, ...args: any[]) => {
    if (isDevelopment) {
      console.info(`[INFO] ${message}`, ...args);
    }
  },
  
  error: (message: string, error?: any) => {
    if (isDevelopment) {
      console.error(`[ERROR] ${message}`, error);
    }
    // Here you could also send errors to a monitoring service
  },
  
  warn: (message: string, ...args: any[]) => {
    if (isDevelopment) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  }
};
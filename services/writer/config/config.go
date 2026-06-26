package config

import "os"

type Config struct {
	GRPCPort    string
	DatabaseURL string
}

func Load() *Config {
	return &Config{
		GRPCPort:    getEnv("GRPC_PORT", ":50051"),
		DatabaseURL: getEnv("DATABASE_URL", "postgres://ml_models:ml_models@localhost:5432/ml_models"),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

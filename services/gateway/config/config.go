package config

import "os"

type Config struct {
	HTTPPort   string
	WriterAddr string
}

func Load() *Config {
	return &Config{
		HTTPPort:   getEnv("HTTP_PORT", ":8080"),
		WriterAddr: getEnv("WRITER_ADDR", "localhost:50051"),
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

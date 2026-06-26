# Build stage — compile the Go binary
FROM golang:1.23-alpine AS build

WORKDIR /app

# Copy generated proto Go code (shared dependency)
COPY protos/protos_go/ protos/protos_go/

# Copy writer source code and module files
COPY services/writer/ services/writer/

WORKDIR /app/services/writer

# Resolve dependencies, download them, and compile the binary
RUN go mod tidy && go build -o /writer cmd/main.go

# Runtime stage — minimal image with just the binary
FROM alpine:3.20

COPY --from=build /writer /writer

EXPOSE 50051

ENTRYPOINT ["/writer"]

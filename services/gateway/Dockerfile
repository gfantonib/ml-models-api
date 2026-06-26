# Multi-stage build: first stage compiles, second stage runs

# Start from Go 1.23 on Alpine (small image with Go toolchain)
FROM golang:1.23-alpine AS build

# Set /app as the working directory inside the container
WORKDIR /app

# Copy the generated protobuf Go code that the gateway imports
# This lives outside the gateway dir, so we need it in the build context
COPY protos/protos_go/ protos/protos_go/

# Copy gateway source code and module files
COPY services/gateway/ services/gateway/

# Move into the gateway directory for all subsequent commands
WORKDIR /app/services/gateway

# Resolve dependencies, download them, and compile the binary
RUN go mod tidy && go build -o /gateway cmd/main.go

# Second stage: minimal runtime image (no Go toolchain, ~7MB base)
FROM alpine:3.20

# Copy only the compiled binary from the build stage
COPY --from=build /gateway /gateway

# Document that the container listens on port 8080
EXPOSE 8080

# Run the gateway binary when the container starts
ENTRYPOINT ["/gateway"]

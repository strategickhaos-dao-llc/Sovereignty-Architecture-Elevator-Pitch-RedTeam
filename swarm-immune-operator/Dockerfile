# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /workspace

# Install build dependencies
RUN apk add --no-cache git ca-certificates

# Copy go module files first for better caching
COPY go.mod go.mod
COPY go.sum go.sum

# Download dependencies
RUN go mod download

# Copy source code
COPY cmd/ cmd/
COPY pkg/ pkg/

# Build the operator binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s" \
    -o /workspace/immune-operator \
    ./cmd/operator/main.go

# Runtime stage - use distroless for minimal attack surface
FROM gcr.io/distroless/static:nonroot

WORKDIR /

# Copy the binary from the builder
COPY --from=builder /workspace/immune-operator /immune-operator

# Run as non-root user
USER 65532:65532

# Expose metrics and health ports
EXPOSE 8080 8081

# Set the entrypoint
ENTRYPOINT ["/immune-operator"]

# Based on go 1.21
FROM golang:1.21

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /forecast-server

EXPOSE 8000
# Runtime
CMD ["/forecast-server"]


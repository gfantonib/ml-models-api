package main

import (
	_ "embed"
	"log"
	"net/http"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "ml-models-api/protos/protos_go/writer"
	"ml-models-api/services/gateway/config"
	"ml-models-api/services/gateway/handler"
)

//go:embed swagger.json
var swaggerSpec []byte

//go:embed swagger.html
var swaggerHTML []byte

func main() {
	cfg := config.Load()

	conn, err := grpc.NewClient(cfg.WriterAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("failed to connect to writer: %v", err)
	}
	defer conn.Close()

	writerClient := pb.NewWriterClient(conn)
	h := handler.NewHandler(writerClient)

	mux := http.NewServeMux()
	mux.HandleFunc("POST /fit", h.Fit)
	mux.HandleFunc("POST /predict", h.Predict)

	mux.HandleFunc("GET /swagger.json", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write(swaggerSpec)
	})
	mux.HandleFunc("GET /swagger", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")
		w.Write(swaggerHTML)
	})

	log.Printf("gateway listening on %s", cfg.HTTPPort)
	log.Println("swagger UI: http://localhost:8080/swagger")
	log.Fatal(http.ListenAndServe(cfg.HTTPPort, mux))
}

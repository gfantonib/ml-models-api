package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"

	pb "ml-models-api/protos/protos_go/writer"
	"ml-models-api/services/writer/config"
	"ml-models-api/services/writer/db"
	"ml-models-api/services/writer/service"
)

func main() {
	cfg := config.Load()

	ctx := context.Background() // A context is a shared control object that defines the lifetime and execution constraints of a group of operations.
	pg, err := db.NewPostgres(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("failed to connect to postgres: %v", err)
	}
	defer pg.Close()

	lis, err := net.Listen("tcp", cfg.GRPCPort)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	srv := grpc.NewServer()
	pb.RegisterWriterServer(srv, service.NewWriterService(pg))

	log.Printf("writer listening on %s", cfg.GRPCPort)
	if err := srv.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

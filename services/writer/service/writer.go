package service

import (
	"context"
	"log"

	"ml-models-api/services/writer/db"

	pb "ml-models-api/protos/protos_go/writer"
)

type WriterService struct {
	pb.UnimplementedWriterServer
	pg *db.Postgres
}

func NewWriterService(pg *db.Postgres) *WriterService {
	return &WriterService{pg: pg}
}

func (s *WriterService) WriteFitInput(ctx context.Context, req *pb.WriteFitInputRequest) (*pb.WriteFitInputResponse, error) {
	result, err := s.pg.InsertFitInput(ctx, req.UserId, req.ModelName, req.Data)
	if err != nil {
		log.Printf("[WRITER] WriteFitInput error: %v", err)
		return nil, err
	}

	log.Printf("[WRITER] WriteFitInput section_id=%s fit_input_id=%s", result.SectionID, result.FitInputID)

	return &pb.WriteFitInputResponse{
		SectionId:  result.SectionID,
		FitInputId: result.FitInputID,
	}, nil
}

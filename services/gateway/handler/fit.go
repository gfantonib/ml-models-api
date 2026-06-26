package handler

import (
	"encoding/json"
	"io"
	"log"
	"net/http"

	pb "ml-models-api/protos/protos_go/writer"
	"ml-models-api/services/gateway/validator"
)

type FitRequest struct {
	UserID    string          `json:"user_id"`
	ModelName string          `json:"model_name"`
	Data      json.RawMessage `json:"data"`
}

func (h *Handler) Fit(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "failed to read body", http.StatusBadRequest)
		return
	}

	var req FitRequest
	if err := json.Unmarshal(body, &req); err != nil {
		http.Error(w, "invalid JSON", http.StatusBadRequest)
		return
	}

	_, err = validator.ValidateFitInput(req.ModelName, req.Data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	resp, err := h.writer.WriteFitInput(r.Context(), &pb.WriteFitInputRequest{
		UserId:    req.UserID,
		ModelName: req.ModelName,
		Data:      req.Data,
	})
	if err != nil {
		log.Printf("[FIT] writer error: %v", err)
		http.Error(w, "failed to write fit input", http.StatusInternalServerError)
		return
	}

	log.Printf("[FIT] section_id=%s fit_input_id=%s", resp.SectionId, resp.FitInputId)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"section_id":   resp.SectionId,
		"fit_input_id": resp.FitInputId,
	})
}

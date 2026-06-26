package handler

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"

	"ml-models-api/services/gateway/validator"
)

type PredictRequest struct {
	UserID    string `json:"user_id"`
	ModelName string `json:"model_name"`
	SectionID string `json:"section_id"`
}

func (h *Handler) Predict(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "failed to read body", http.StatusBadRequest)
		return
	}

	var req PredictRequest
	if err := json.Unmarshal(body, &req); err != nil {
		http.Error(w, "invalid JSON", http.StatusBadRequest)
		return
	}

	if err := validator.ValidateModelName(req.ModelName); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	log.Printf("[PREDICT] user_id=%s model=%s section_id=%s", req.UserID, req.ModelName, req.SectionID)

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "predict accepted for model %s, section %s\n", req.ModelName, req.SectionID)
}

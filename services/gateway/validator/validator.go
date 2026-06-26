package validator

import (
	"fmt"

	models "ml-models-api/protos/protos_go/models"

	"google.golang.org/protobuf/encoding/protojson"
	"google.golang.org/protobuf/proto"
)

var registry = map[string]func() proto.Message{
	"ANT_COLONY_MODEL":                  func() proto.Message { return &models.AntColonyRequest{} },
	"PYTHAGOREAN_SUPPORT_MACHINE_MODEL": func() proto.Message { return &models.PythagoreanSupportMachineInput{} },
}

func ValidateFitInput(modelName string, data []byte) (proto.Message, error) {
	factory, ok := registry[modelName]
	if !ok {
		return nil, fmt.Errorf("unknown model: %s", modelName)
	}

	msg := factory()
	if err := protojson.Unmarshal(data, msg); err != nil {
		return nil, fmt.Errorf("invalid data for %s: %w", modelName, err)
	}

	return msg, nil
}

func ValidateModelName(modelName string) error {
	if _, ok := registry[modelName]; !ok {
		return fmt.Errorf("unknown model: %s", modelName)
	}
	return nil
}

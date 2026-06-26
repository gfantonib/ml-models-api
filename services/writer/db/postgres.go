package db

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Postgres struct {
	pool *pgxpool.Pool
}

func NewPostgres(ctx context.Context, databaseURL string) (*Postgres, error) {
	pool, err := pgxpool.New(ctx, databaseURL)
	if err != nil {
		return nil, fmt.Errorf("unable to connect to database: %w", err)
	}
	if err := pool.Ping(ctx); err != nil {
		return nil, fmt.Errorf("unable to ping database: %w", err)
	}
	return &Postgres{pool: pool}, nil
}

func (p *Postgres) Close() {
	p.pool.Close()
}

type FitInputResult struct {
	SectionID  string
	FitInputID string
}

func (p *Postgres) InsertFitInput(ctx context.Context, userID, modelName string, data []byte) (*FitInputResult, error) {
	tx, err := p.pool.Begin(ctx)
	if err != nil {
		return nil, fmt.Errorf("begin tx: %w", err)
	}
	defer tx.Rollback(ctx)

	var sectionID string
	err = tx.QueryRow(ctx,
		"INSERT INTO sections (user_id, model_name) VALUES ($1, $2) RETURNING id",
		userID, modelName,
	).Scan(&sectionID)
	if err != nil {
		return nil, fmt.Errorf("insert section: %w", err)
	}

	var fitInputID string
	err = tx.QueryRow(ctx,
		"INSERT INTO fit_inputs (section_id, data) VALUES ($1, $2) RETURNING id",
		sectionID, data,
	).Scan(&fitInputID)
	if err != nil {
		return nil, fmt.Errorf("insert fit_input: %w", err)
	}

	if err := tx.Commit(ctx); err != nil {
		return nil, fmt.Errorf("commit tx: %w", err)
	}

	return &FitInputResult{SectionID: sectionID, FitInputID: fitInputID}, nil
}

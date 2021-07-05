package service

import (
	"context"
	"gorm.io/gorm"
)

//${service}Service should implement the Service interface


type ${service}Service struct {
	DB *gorm.DB
}

type Service interface {
	${endpoints}
}
package middlewares

import (
    //import the service package
    "${module}/internal/service"
	"github.com/go-kit/kit/log"
)

type LoggingMiddleware struct {
	Logger log.Logger
	Next   service.Service
}


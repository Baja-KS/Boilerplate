package main

import (
    "${module}/internal/database"
    "${module}/internal/service"
    "${module}/internal/service/middlewares"
	"${module}/internal/service/endpoints"
    "${module}/internal/service/transport"
	"github.com/go-kit/kit/log"
	"net/http"
	"os"
)


func main() {
	logger:=log.NewLogfmtLogger(os.Stderr)
	var err error
	db,err:=database.NewDatabase()
	if err != nil {
		log.With(logger,"err",err)
	}
	err=database.Migrate(db)
	if err != nil {
		log.With(logger,"err",err)
	}

	var svc service.Service
	svc= &middlewares.LoggingMiddleware{Logger: logger, Next: &service.${service}Service{DB: db}}

	ep:=endpoints.NewEndpointSet(svc)
	err = http.ListenAndServe(":8080", transport.NewHTTPHandler(ep))
	if err != nil {
		log.With(logger,"err",err)
	}
	log.With(logger,"msg","Listening to port")
}

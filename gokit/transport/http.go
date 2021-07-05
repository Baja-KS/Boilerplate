package transport

import (
	"${module}/internal/service/endpoints"
	httptransport "github.com/go-kit/kit/transport/http"
	"github.com/gorilla/mux"
	"net/http"
)

func NewHTTPHandler(ep endpoints.EndpointSet) http.Handler {
	router:=mux.NewRouter()

	${handlers}

	${router}

	return router
}
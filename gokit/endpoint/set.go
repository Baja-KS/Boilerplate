type EndpointSet struct {
	${endpoints}
}

func NewEndpointSet(svc service.Service) EndpointSet {
	return EndpointSet{
		${endpointfactories}
	}
}
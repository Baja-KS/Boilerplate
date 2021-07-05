func Make${endpoint}Endpoint(svc service.Service) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (response interface{}, err error) {
        req:=request.(${endpoint}Request)

		return ${endpoint}Response{},nil
	}
}
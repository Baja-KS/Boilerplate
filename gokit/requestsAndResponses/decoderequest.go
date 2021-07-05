func Decode${endpoint}Request(ctx context.Context, r *http.Request) (interface{}, error) {
	var request ${endpoint}Request
	err:=json.NewDecoder(r.Body).Decode(&request)
	if err != nil {
		return nil, err
	}
	return request,nil
}
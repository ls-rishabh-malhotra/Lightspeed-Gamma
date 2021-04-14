package main

import "example.com/go-service/cmd/service"

func main() {
	s := service.New()
	s.Initialize()
	s.Start()
}

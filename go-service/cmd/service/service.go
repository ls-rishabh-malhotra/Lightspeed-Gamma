package service

import (
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"

	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"

	"example.com/go-service/pkg/routes"
)

type Service struct {
	 EchoServer *echo.Echo
	 Router *routes.Routes
}

func New() *Service {
	return &Service{}
}

func (s *Service) Initialize() {
	s.EchoServer = initEcho()
	s.Router = routes.NewRouter(s.EchoServer)
	s.Router.Map()
}

func initEcho() *echo.Echo {
	e := echo.New()
	// Logger
	e.Use(middleware.Logger())
	// Recover
	e.Use(middleware.Recover())
	// CORS
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{echo.POST, echo.GET},
	}))

	return e
}

func (s *Service) Start() {
	wg := sync.WaitGroup{}
	wg.Add(1)

	go func() {
		defer wg.Done()
		if err := s.EchoServer.Start(":8081"); err != nil && err != http.ErrServerClosed {
			// log error
		}
	}()

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	<-c
	s.EchoServer.Close()
}
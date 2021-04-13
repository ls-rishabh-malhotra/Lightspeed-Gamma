package routes

import (
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/labstack/echo"
)

type Router interface {
	Map()
}

type Routes struct {
	Echo *echo.Echo
}

func NewRouter(echo *echo.Echo) *Routes {
	return &Routes{
		Echo: echo,
	}
}

func (r Routes) Map() {
	r.Echo.GET("/checks/ready", readinessCheck)
	r.Echo.GET("/checks/live", livelinessCheck)

	v1 := r.Echo.Group("/v1")

	for _, grp := range []*echo.Group{v1} {
		grp.POST("/product_image", queryProductInfo)
	}
}

func livelinessCheck(c echo.Context) error {
	return c.JSON(http.StatusOK, "the application is live")
}

func readinessCheck(c echo.Context) error {
	return c.JSON(http.StatusOK, "the application is ready")
}


func queryProductInfo(c echo.Context) error {
	file, err := c.FormFile("file")
	if err != nil {
		// handle error
	}

	// send file to gamma endpoint and parse response

	// mock implementation to prevent error of file not being used
	src, err := file.Open()
	if err != nil {
		// handle error
	}
	defer src.Close()

	dst, err := os.Create(file.Filename)
	if err != nil {
		// handle error
	}
	defer dst.Close()

	if _, err = io.Copy(dst, src); err != nil {
		return err
	}

	return c.JSON(http.StatusOK, fmt.Sprintf("File %s uploaded successfully.", file.Filename))
}



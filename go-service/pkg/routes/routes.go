package routes

import "github.com/labstack/echo"

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
	v1 := r.Echo.Group("/v1")

	for _, grp := range []*echo.Group{v1} {
		grp.POST("/product_image", queryProductInfo)
	}
}


func queryProductInfo(c echo.Context) error {
	// TODO: implement image upload and call gamma endpoint for product info
	return nil
}


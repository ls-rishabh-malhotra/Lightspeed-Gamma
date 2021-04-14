package routes

import (
	"context"
	"fmt"
	"io"
	"net/http"

	"cloud.google.com/go/storage"
	"github.com/labstack/echo"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/option"
)

const gcsBucketName = "ls-inno-week-gamma-image-upload"
const imageName = "imgToQuery.jpg"

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
	ctx := context.Background()

	file, err := c.FormFile("file")
	if err != nil {
		fmt.Println("file could not be fetched from form")
		fmt.Println(err)
	}

	blobFile, err := file.Open()
	if err != nil {
		fmt.Println("file could not be opened")
		fmt.Println(err)
	}
	defer blobFile.Close()


	storageCredentials, err := google.FindDefaultCredentials(context.Background(), storage.ScopeReadWrite)
	if err != nil {
		fmt.Println("could not find storage credentials")
		fmt.Println(err)
	}
	fmt.Println("found storage credentials")

	storageClient, err := storage.NewClient(context.Background(), option.WithCredentials(storageCredentials))
	if err != nil {
		fmt.Println("could not make storage client")
	}
	fmt.Println("successfully made storage client")

	imgWriter := storageClient.Bucket(gcsBucketName).Object(imageName).NewWriter(ctx)
	if _, err := io.Copy(imgWriter, blobFile); err != nil {
		fmt.Println("failed to copy file to imgWriter")
		fmt.Println(err)
	}
	if err := imgWriter.Close(); err != nil {
		fmt.Println("failed to close imgWriter")
		fmt.Println(err)
	}

	return c.JSON(http.StatusOK, "uploaded to bucket")
}



package main

import (
  "fmt"
  "net/http"
  "github.com/gin-gonic/gin"
)

// using gin (similar to express.js but for go)
// https://github.com/gin-gonic/gin/blob/v1.10.0/docs/doc.md

func main() {
  router := gin.Default()
  router.GET("/ping", func(c *gin.Context) {
      c.String(http.StatusOK, "pong")
  })
  router.Run(":8080")
  // TODO: Put this in .env
}

func handler(w http.ResponseWriter, r *http.Request) {
  fmt.Fprint(w, "Hello, World!")
}

func testHandler(w http.ResponseWriter, r *http.Request) {
  fmt.Fprint(w, "Testing")
}

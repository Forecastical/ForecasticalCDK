package main // package name declaration.


// READ!!
// Most of the important info on maintaning and deving is from this guide:
// https://go.dev/doc/tutorial/web-service-gin


// imports
import (
    "net/http"
    //"fmt"
    "time"
    "github.com/gin-gonic/gin"
)

// data structs
type region struct {
  Name  string  `json:"name"`
  Lat   float32 `json:"lat"`
  Lon   float32 `json:"lon"`
  Ctry  string  `json:"country"`
  State string  `json:"state"`
}
type forecast struct {
  Region region `json:"region"`
}
type hourForecast struct {
  ID string `json:"id"`
  Region region `json:"region"`
  Timestamp time.Time `json:"timestamp"`
  Temp float32 `json:"temp"`
}
type dayForecast struct {
  ID string `json:"id"`
  Region region `json:"region"`
  Timestamp time.Time `json:"timestamp"`
  TMax      float32   `json:"tmax"` // Max temp for the day in Kelvin
  TMin      float32   `json:"tmin"`
  Sunrise   time.Time `json:"sunrise"`
  Sunset    time.Time `json:"sunset"`
  Summary   string `json:"summary"`
}
// Fake data
var hForecastA = hourForecast {
  ID: "1",
  Region: region {

  },
  Timestamp: time.Now(),
  Temp: 288.706,
}

// functions
func getHourForecast(c *gin.Context) {
  c.IndentedJSON(http.StatusOK, hForecastA)
}
// takes gin.Context

// runtime
func main() {
    router := gin.Default()
    // Example; router.GET("/albums", getAlbums)
    router.GET("/hour", getHourForecast)

    router.Run("0.0.0.0:8080")
}

package main // package name declaration.


// READ!!
// Most of the important info on maintaning and deving is from this guide:
// https://go.dev/doc/tutorial/web-service-gin


// imports
import (
    //"net/http"
    //"fmt"
    "time"
    "github.com/gin-gonic/gin"
    //owm "github.com/briandowns/openweathermap"
)
// const 
//const weatherAPIEndpoint = "http://api.weatherapi.com/v1"
const weatherAPIEndpoint = "https://api.open-meteo.com/v1/"
//const geolocateAPIEndpoint = "https://ip-api.com/"
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
  Condition condition `json:"condition"`
  Summary   string `json:"summary"`
}

type currentForecast struct {
  ID string `json:"id"`
  Region region `json:"region"`
  Timestamp time.Time `json:"timestamp"`
  Temp float32 `json:"temp"`
}


type condition struct {
  AQI int `json:"aqi"`
  UVI int `json:"uvi"`
  Humidity float32 `json:"humidity"`
  Pressure float32 `json:"pressure"`
}

type post struct {
  ID string `json:"id"`
  Caption string `json:"caption"`
  Author  user  `json:"author"`
  Region region `json:"region"`
  Timestamp time.Time `json:"timestamp"`
}

type user struct {
  ID string `json:"id"`
  Username string `json:"username"`
  HomeRegion region `json:"homeRegion"`
  PreferredTemp   float32   `json:"preferredTemp`
  Units   string  `json:"units"`
  //Alerts  a
}
// Fake data
var regionA = region {
  Name: "London, OH",
  Lat: 0.0,
  Lon: 0.0,
  Ctry: "United States",
  State: "Ohio",
}

var regionB = region {
  Name: "Columbus, OH",
  Lat: 1.2,
  Lon: 3.4,
  Ctry: "United States",
  State: "Ohio",
}

var regionC = region {
  Name: "Dublin, OH",
  Lat: 1.0,
  Lon: 3.0,
  Ctry: "United States",
  State: "Ohio",
}

var hForecastA = hourForecast {
  ID: "1",
  Region: regionA,
  Timestamp: time.Now(),
  Temp: 288.706,
}
var hForecastB = hourForecast {
  ID: "2",
  Region: regionB,
  Timestamp: time.Now(),
  Temp: 288.706,
}
var hForecastC = hourForecast {
  ID: "3",
  Region: regionC,
  Timestamp: time.Now(),
  Temp: 288.706,
}

var dForecastA = dayForecast {
  ID: "1",
  Region: regionA,
  Timestamp: time.Now(),
  TMax: 298.706,
  TMin: 238.706,
  Sunrise: time.Now(),
  Sunset: time.Now(),
  Summary: "Sunny",
}

var dForecastB = dayForecast {
  ID: "2",
  Region: regionB,
  Timestamp: time.Now(),
  TMax: 298.706,
  TMin: 238.706,
  Sunrise: time.Now(),
  Sunset: time.Now(),
  Summary: "Sunny",
}

var dForecastC = dayForecast {
  ID: "3",
  Region: regionC,
  Timestamp: time.Now(),
  TMax: 298.706,
  TMin: 238.706,
  Sunrise: time.Now(),
  Sunset: time.Now(),
  Summary: "Sunny",
}
// functions
// takes gin.Context
//func getLocation(c *gin.Context) {
//  // const locationResponse = await fetch(`http://api.weatherapi.com/v1/ip.json?key=${apiKey}&q=auto:ip`);
//  // Input: IP address
//  // Output: Location data from OpenWeatherMap API
//
//  // Get the IP address from the request
//  //const ip = c.Request.ip;
//  
//  // Get the location data from the OpenWeatherMap API
//  return null;
//}

// runtime
func main() {
    router := gin.Default()
    // Example; router.GET("/albums", getAlbums)
    //router.GET("/hour", getHourForecast)
    //router.GET("/day", getDayForecast)
    // GET /ping
    router.GET("/ping", func(c *gin.Context) {
      c.JSON(200, gin.H{
        "message": "pong",
      })
    })
    // GET /
    router.GET("/", func(c *gin.Context) {
      c.JSON(200, gin.H{
        "message": "Welcome to the Weather API",
      })
    })
    router.Run("0.0.0.0:8000")
  }

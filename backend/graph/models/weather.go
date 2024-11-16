package models

//type Region {
//  lat: String!
//  lon: String!
//}
//
//type Weather {
//  temp: String!
//  condition: String!
//  aqi: String!
//  uvi: String!
//  humidity: String!
//  pressure: String!
//}
//
//type Forecast {
//  id: ID!
//  region: Region!
//  timestamp: String!
//  weather: Weather!
//}


type User struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Region struct {
  lat  string `json:"lat"`
  lon  string `json:"lon"`
}

type Weather struct {
  temp string `json:"string"`
  condition string `json:"string"`
  aqi string `json:"string"`
  uvi string `json:"string"`
  humidity string `json:"string"`
  pressure string `json:"string"`
}

type Forecast struct {
  id string `json:"id"`
  region *Region `json:"region"`
  timestamp string `json:"timestamp"`
  weather *Weather `json:"weather"`
}

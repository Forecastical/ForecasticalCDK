package main

import (
	"log"
	"net/http"
	"os"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/Forecastical/ForecasticalBackend/graph"
)
// https://medium.com/@krishnan.srm/graphql-with-golang-331de956d956

const defaultPort = "8080"

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	srv := handler.NewDefaultServer(graph.NewExecutableSchema(graph.Config{Resolvers: &graph.Resolver{}}))

	http.Handle("/", playground.Handler("GraphQL playground", "/query"))
	http.Handle("/query", srv) //  GraphQL servers only have one api-endpoint.

	log.Printf("connect to http://localhost:%s/ for GraphQL playground", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

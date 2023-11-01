package main

import (
	"time"
)

type Cloud struct{}

type CloudsCache struct {
	clouds []Cloud
}

var cloudsCache CloudsCache = CloudsCache{
	clouds: nil,
}

func getClouds(cacheAvailableChannel chan bool) []Cloud {
	if cloudsCache.clouds == nil {
		cacheAvailable := <-cacheAvailableChannel

		if !cacheAvailable {
			updateCacheFromExternalService(cacheAvailableChannel)
		}
	}
	return cloudsCache.clouds
}

func updateCacheFromExternalService(cacheAvailableChannel chan<- bool) {
	time.Sleep(3 * time.Second)
	cloudsCache.clouds = []Cloud{}

	cacheAvailableChannel <- true
	close(cacheAvailableChannel)
}

func main() {
	cacheAvailableChannel := make(chan bool)
	cacheAvailableChannel <- false

	for i := 0; i < 10; i++ {
		go getClouds(cacheAvailableChannel)
	}
}

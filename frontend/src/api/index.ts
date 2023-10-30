import {
  SearchCloudsResult, SearchCloudRequest, searchClouds
} from "./clouds"

import {
  ApiErrors, hasApiErrors, 
} from "./errors"

class Config {
  constructor(public baseUrl: string) {}
}
class Api {
  constructor(public config: Config) {}

  searchClouds(request: SearchCloudRequest): Promise<SearchCloudsResult> {
    return searchClouds(this.config.baseUrl, request);
  }
}

function getApi(config: Config): Api {
  return new Api(config);
}

const api = getApi({baseUrl: "http://localhost:8080"})

export {
  api, hasApiErrors
}

export type {
  ApiErrors, SearchCloudRequest, SearchCloudsResult
}

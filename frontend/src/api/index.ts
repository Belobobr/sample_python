import { Cloud } from '../entities';

class ApiError {
  constructor(public message: string, public status: number, public more_info?: string) {}
}

// cloud

class Clouds {
  constructor(public clouds: Cloud[], public errors?: ApiError[], public message?: string) {}
}

// search api

class CloudFilter {
  constructor(public provider?: string) {}
}

class CloudRequestFilter {
  constructor(public cloud?: CloudFilter) {}
}

class CloudRequestSort {
  constructor(public user_geo_latitude?: number, public user_geo_longitude?: number) {}
}

class SearchCloudsRequest {
  constructor(public filter?: CloudRequestFilter, public sort?: CloudRequestSort) {}
}

class SearchCloudsResponse extends Clouds {
  constructor(public clouds: Cloud[], public errors: ApiError[], public message: string) {
    super(clouds, errors, message);
  }
}

// api implementation

class Result<T> {
  constructor(public body: T, public status: number) {}
}

class Config {
  constructor(public domain: string) {}
}

class Api {
  constructor(public config: Config) {}

  // public getDomain(): string {
  //     return this.config.domain;
  // }

  public async searchClouds(request: SearchCloudsRequest): Promise<Result<SearchCloudsResponse>> {
    const url = `${this.config.domain}/api/clouds:search`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    const body = (await response.json()) as SearchCloudsResponse;
    const status = response.status;
    return new Result(body, status);
  }
}

function getApi(config: Config): Api {
  return new Api(config);
}

export { getApi };

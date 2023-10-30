import { SearchCloudsRequest, SearchCloudsResponseBody } from './clouds'

class ServerApiError {
  constructor(public message: string, public status: number, public more_info?: string) {}
}

class Result<T> {
  constructor(public body: T, public status: number) {}
}

class Config {
  constructor(public baseUrl: string) {}
}

class Api {
  constructor(public config: Config) {}

  public async searchClouds(request: SearchCloudsRequest): Promise<Result<SearchCloudsResponseBody>> {
    const url = `${this.config.baseUrl}/api/clouds:search`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    const body = (await response.json()) as SearchCloudsResponseBody;
    const status = response.status;
    return new Result(body, status);
  }
}

function getApi(config: Config): Api {
  return new Api(config);
}

const api = getApi({baseUrl: "http://localhost:8080"})

export {
  api, SearchCloudsRequest, SearchCloudsResponseBody as SearchCloudsResponse, ServerApiError
}

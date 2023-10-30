import { Cloud, CloudFilter, CloudSort } from '../entities';
import { ServerResponse, CommonResponseBody, ResponseBodyError, makePostRequest } from './server';
import { makeRequestWithErrorsHandling, ApiResult } from './errors';

class Clouds {
  constructor(public clouds: Cloud[], public errors?: ResponseBodyError[], public message?: string) {}
}

interface SearchCloudRequest {
  filter?: CloudFilter;
  sort?: CloudSort;
}

type SearchCloudsResult = ApiResult<Cloud[]>;

// search clouds implementation

class SearchCloudsRequestBody implements SearchCloudRequest {
  constructor(public filter?: CloudFilter, public sort?: CloudSort) {}
}
class SearchCloudsResponseBody extends Clouds implements CommonResponseBody {
  constructor(public clouds: Cloud[], public errors: ResponseBodyError[], public message: string) {
    super(clouds, errors, message);
  }
}

async function searchClouds(baseUrl: string, request: SearchCloudsRequestBody): Promise<SearchCloudsResult> {
  return makeRequestWithErrorsHandling<SearchCloudsResponseBody, Cloud[]>(
    () => searchCloudsRequest(baseUrl, request),
    (responseBody) => responseBody.clouds,
  );
}

async function searchCloudsRequest(
  baseUrl: string,
  request: SearchCloudsRequestBody,
): Promise<ServerResponse<SearchCloudsResponseBody>> {
  return makePostRequest(baseUrl, 'api/clouds:search', request);
}

export { searchClouds };

export type { SearchCloudsResult, SearchCloudRequest };

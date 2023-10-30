import { Cloud, CloudFilter, CloudSort } from '../entities';
import { api, ServerApiError } from '../api';

// cloud

class Clouds {
    constructor(public clouds: Cloud[], public errors?: ServerApiError[], public message?: string) {}
}
  
// search api
class SearchCloudsRequest {
    constructor(public filter?: CloudFilter, public sort?: CloudSort) {}
}

class SearchCloudsResponseBody extends Clouds {
    constructor(public clouds: Cloud[], public errors: ServerApiError[], public message: string) {
        super(clouds, errors, message);
    }
}

// api errors handling

// TODO - implement error rendering component
interface ApiErrors {
    serverErrors?: ServerApiError[]
    status?: number
    clientError?: string
}

function hasServiceErrors(serviceErrors: ApiErrors): boolean {
    return Object.keys(serviceErrors).length > 0;
}


// search clouds implementation
  
interface SearchCloudsResult {
    errors: ApiErrors;
    clouds: Cloud[];
}
  
  //TODO make part of api module, split api into a few levels...
async function searchClouds(request: SearchCloudsRequest): Promise<SearchCloudsResult> {

  let errors: ApiErrors = {}
  let clouds: Cloud[] = []

  try {
    let result = await api.searchClouds(request);

    if (result.body.errors) {  
      errors.serverErrors = result.body.errors;
    }
    
    if (result.status === 200) {
      clouds = result.body.clouds;
    } else {
      errors.status = result.status
    }

  } catch (e: any) {
    errors.clientError = e.message;
  }

  return {
    errors,
    clouds: []
  }
}

export { SearchCloudsRequest, SearchCloudsResponseBody, searchClouds, hasServiceErrors }
export type { SearchCloudsResult, ApiErrors as ServiceErrors }
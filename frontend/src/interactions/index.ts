import { Cloud } from '../entities';
import { api, SearchCloudsRequest, ApiError } from '../api';


// search clouds module
// TODO - implement error rendering component
interface ServiceErrors {
    apiErrors?: ApiError[]
    status?: number
    uiError?: string
  }
  
interface SearchCloudsResult {
  errors: ServiceErrors;
  clouds: Cloud[];
}

function hasServiceErrors(serviceErrors: ServiceErrors): boolean {
  return Object.keys(serviceErrors).length > 0;
}
  
  //TODO make part of api module, split api into a few levels...
async function searchClouds(request: SearchCloudsRequest): Promise<SearchCloudsResult> {

  let errors: ServiceErrors = {}
  let clouds: Cloud[] = []

  try {
    let result = await api.searchClouds(request);

    if (result.body.errors) {  
      errors.apiErrors = result.body.errors;
    }
    
    if (result.status === 200) {
      clouds = result.body.clouds;
    } else {
      errors.status = result.status
    }

  } catch (e: any) {
    errors.uiError = e.message;
  }

  return {
    errors,
    clouds: []
  }
}

export { searchClouds, hasServiceErrors }
export type { SearchCloudsResult, ServiceErrors }
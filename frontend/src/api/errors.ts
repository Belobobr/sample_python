//
import { ServerResponse, CommonResponseBody, ResponseBodyError } from './server';

interface ApiErrors {
  serverErrors?: ResponseBodyError[];
  statusError?: number;
  clientError?: string;
}

interface ApiResult<Result> {
  result: Result;
  errors: ApiErrors;
}

async function makeRequestWithErrorsHandling<ResponseBody extends CommonResponseBody, Result>(
  makeRequest: () => Promise<ServerResponse<ResponseBody>>,
  getResult: (responseBody: ResponseBody) => Result,
): Promise<ApiResult<Result>> {
  const errors: ApiErrors = {};
  let result: Result = {} as Result;

  try {
    const response = await makeRequest();

    if (response.body.errors) {
      errors.serverErrors = response.body.errors;
    }

    if (response.status === 200) {
      result = getResult(response.body);
    } else {
      errors.statusError = response.status;
    }
  } catch (e) {
    errors.clientError = getErrorMessage(e);
  }

  return {
    errors,
    result,
  };
}

function hasApiErrors(serviceErrors: ApiErrors): boolean {
  return Object.keys(serviceErrors).length > 0;
}

export { makeRequestWithErrorsHandling, hasApiErrors };

export type { ApiResult, ApiErrors };

function getErrorMessage(error: unknown) {
  if (error instanceof Error) return error.message;
  return String(error);
}

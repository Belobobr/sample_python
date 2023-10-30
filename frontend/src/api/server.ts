class ServerResponse<T> {
  constructor(public body: T, public status: number) {}
}

interface CommonResponseBody {
  errors?: ResponseBodyError[];
  message?: string;
}

class ResponseBodyError {
  constructor(public message: string, public status: number, public more_info?: string) {}
}

async function makePostRequest<RequestBody, ResponseBody>(
  baseUrl: string,
  path: string,
  body: RequestBody,
): Promise<ServerResponse<ResponseBody>> {
  const url = `${baseUrl}/${path}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const responseBody = (await response.json()) as ResponseBody;
  const status = response.status;
  return new ServerResponse(responseBody, status);
}

export { ServerResponse, ResponseBodyError, makePostRequest };

export type { CommonResponseBody };

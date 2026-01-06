from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_error_response import HttpErrorResponse
from ...models.http_task_update_request import HttpTaskUpdateRequest
from ...models.http_task_update_response import HttpTaskUpdateResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: HttpTaskUpdateRequest,
    task_id: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["task_id"] = task_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/tasks",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HttpErrorResponse | HttpTaskUpdateResponse | None:
    if response.status_code == 200:
        response_200 = HttpTaskUpdateResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = HttpErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = HttpErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = HttpErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HttpErrorResponse | HttpTaskUpdateResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HttpTaskUpdateRequest,
    task_id: str,
) -> Response[HttpErrorResponse | HttpTaskUpdateResponse]:
    """Update task

     Update task information and create history record

    Args:
        task_id (str):
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskUpdateResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        task_id=task_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: HttpTaskUpdateRequest,
    task_id: str,
) -> HttpErrorResponse | HttpTaskUpdateResponse | None:
    """Update task

     Update task information and create history record

    Args:
        task_id (str):
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskUpdateResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        task_id=task_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HttpTaskUpdateRequest,
    task_id: str,
) -> Response[HttpErrorResponse | HttpTaskUpdateResponse]:
    """Update task

     Update task information and create history record

    Args:
        task_id (str):
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskUpdateResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        task_id=task_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: HttpTaskUpdateRequest,
    task_id: str,
) -> HttpErrorResponse | HttpTaskUpdateResponse | None:
    """Update task

     Update task information and create history record

    Args:
        task_id (str):
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskUpdateResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            task_id=task_id,
        )
    ).parsed

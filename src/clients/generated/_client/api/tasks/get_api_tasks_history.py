from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_error_response import HttpErrorResponse
from ...models.http_task_history_response import HttpTaskHistoryResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    task_id: str,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["task_id"] = task_id

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/tasks/history",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HttpErrorResponse | HttpTaskHistoryResponse | None:
    if response.status_code == 200:
        response_200 = HttpTaskHistoryResponse.from_dict(response.json())

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
) -> Response[HttpErrorResponse | HttpTaskHistoryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    task_id: str,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[HttpErrorResponse | HttpTaskHistoryResponse]:
    """Get task history

     Get complete task history including status changes and logs

    Args:
        task_id (str):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskHistoryResponse]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    task_id: str,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> HttpErrorResponse | HttpTaskHistoryResponse | None:
    """Get task history

     Get complete task history including status changes and logs

    Args:
        task_id (str):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskHistoryResponse
    """

    return sync_detailed(
        client=client,
        task_id=task_id,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    task_id: str,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[HttpErrorResponse | HttpTaskHistoryResponse]:
    """Get task history

     Get complete task history including status changes and logs

    Args:
        task_id (str):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskHistoryResponse]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    task_id: str,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> HttpErrorResponse | HttpTaskHistoryResponse | None:
    """Get task history

     Get complete task history including status changes and logs

    Args:
        task_id (str):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskHistoryResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
            limit=limit,
            offset=offset,
        )
    ).parsed

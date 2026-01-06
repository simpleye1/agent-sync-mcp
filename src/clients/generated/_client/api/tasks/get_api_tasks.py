from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_error_response import HttpErrorResponse
from ...models.http_task_status_response import HttpTaskStatusResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    task_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["task_id"] = task_id

    params["session_id"] = session_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/tasks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HttpErrorResponse | HttpTaskStatusResponse | None:
    if response.status_code == 200:
        response_200 = HttpTaskStatusResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = HttpErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = HttpErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HttpErrorResponse | HttpTaskStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    task_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
) -> Response[HttpErrorResponse | HttpTaskStatusResponse]:
    """Get task

     Get task information by task_id or session_id

    Args:
        task_id (str | Unset):
        session_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskStatusResponse]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        session_id=session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    task_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
) -> HttpErrorResponse | HttpTaskStatusResponse | None:
    """Get task

     Get task information by task_id or session_id

    Args:
        task_id (str | Unset):
        session_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskStatusResponse
    """

    return sync_detailed(
        client=client,
        task_id=task_id,
        session_id=session_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    task_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
) -> Response[HttpErrorResponse | HttpTaskStatusResponse]:
    """Get task

     Get task information by task_id or session_id

    Args:
        task_id (str | Unset):
        session_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskStatusResponse]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
        session_id=session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    task_id: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
) -> HttpErrorResponse | HttpTaskStatusResponse | None:
    """Get task

     Get task information by task_id or session_id

    Args:
        task_id (str | Unset):
        session_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskStatusResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
            session_id=session_id,
        )
    ).parsed

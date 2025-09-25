

from __future__ import annotations

import contextlib
import dataclasses
import os
from typing import cast, Dict, Any, Optional

import httpx
import reflex as rx

VERIFY_ENDPOINT = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
SITE_KEY = os.environ.get("TURNSTILE_SITE_KEY")
SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY")


def set_site_key(site_key: str):
    global SITE_KEY
    SITE_KEY = site_key


def set_secret_key(secret_key: str):
    global SECRET_KEY
    SECRET_KEY = secret_key


def is_key_set() -> bool:
    return bool(SITE_KEY) and bool(SECRET_KEY)


class TurnstileState(rx.State):
    _is_valid: bool = False
    _current_token: str = ""
    _error_message: str = ""

    @rx.event
    async def verify_token(self, token: str):
        if not is_key_set():
            raise RuntimeError(
                "Cannot validate tokens without setting site and secret keys."
            )

        self._current_token = token
        self._error_message = ""

        payload = {
            "secret": SECRET_KEY,
            "response": token,
            "remoteip": getattr(
                self.router.headers, "x_forwarded_for", self.router.session.client_ip
            ),
        }

        async with httpx.AsyncClient() as aclient:
            resp = await aclient.post(VERIFY_ENDPOINT, data=payload)
            resp.raise_for_status()



        with contextlib.suppress(ValueError):
            response_data = resp.json()
            self._is_valid = response_data.get("success", False)

            print(f"Verification result: {self._is_valid}")
            print(f"Full response: {response_data}")

    @rx.event
    def handle_error(self, error_code: str):
        self._error_message = f"Turnstile error: {error_code}"
        self._is_valid = False
        print(f"Turnstile error: {error_code}")

    @rx.var(cache=True)
    def token_is_valid(self) -> bool:
        return self._is_valid

    @rx.var(cache=True)
    def current_token(self) -> str:
        return self._current_token

    @rx.var(cache=True)
    def error_message(self) -> str:
        return self._error_message

    def reset_validation(self):
        self._is_valid = False
        self._current_token = ""
        self._error_message = ""


class Turnstile(rx.Component):


    library = "@marsidev/react-turnstile"

    tag = "Turnstile"

    is_default = False

    site_key: rx.Var[str]


    options: rx.Var[Dict[str, Any]]


    script_options: rx.Var[Dict[str, Any]]


    rerender_on_callback_change: rx.Var[bool]
    as_: rx.Var[str]
    inject_script: rx.Var[bool]

    on_widget_load: rx.EventHandler[lambda widget_id: [widget_id]]
    on_success: rx.EventHandler[lambda token: [token]]
    on_error: rx.EventHandler[lambda error_code: [error_code]]
    on_expire: rx.EventHandler[lambda: []]
    on_timeout: rx.EventHandler[lambda: []]
    on_before_interactive: rx.EventHandler[lambda: []]
    on_after_interactive: rx.EventHandler[lambda: []]
    on_unsupported: rx.EventHandler[lambda: []]
    on_load_script: rx.EventHandler[lambda: []]

    @classmethod
    def create(cls, **props) -> Turnstile:


        if props.get("size") == "invisible":
            props.setdefault("id", rx.vars.get_unique_variable_name())
            raise NotImplementedError("Invisible mode is not currently working.")

        props.setdefault("site_key", SITE_KEY)
        props.setdefault("on_success", TurnstileState.verify_token)


        return cast(Turnstile, super().create(**props))


    def api(self) -> TurnstileAPI:
        ref = self.get_ref()
        if ref:
            return TurnstileAPI(ref_name=self.get_ref())
        raise ValueError("Component must have an ID to use the API.")


turnstile = Turnstile.create

@dataclasses.dataclass(frozen=True, slots=True)
class TurnstileAPI:
    ref_name: str

    def _get_api_spec(self, fn_name) -> rx.Var[rx.EventChain]:
        return rx.Var(
            f"{rx.Var(self.ref_name)._as_ref()}?.current?.{fn_name}",
            _var_type=rx.EventChain,
        )

    def get_value(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("get_value")

    def get_widget_id(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("get_widget_id")

    def reset(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("reset")

    def execute(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("execute")


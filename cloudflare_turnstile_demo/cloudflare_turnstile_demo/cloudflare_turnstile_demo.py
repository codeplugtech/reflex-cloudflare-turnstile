import reflex as rx

import reflex_cloudflare_turnstile
from reflex_cloudflare_turnstile import turnstile, TurnstileState


if not reflex_cloudflare_turnstile.is_key_set():
    reflex_cloudflare_turnstile.set_site_key("3x00000000000000000000FF")
    reflex_cloudflare_turnstile.set_secret_key("1x0000000000000000000000000000000AA")


class State(rx.State):
    pass


def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Reflex Cloudflare Turnstile Demo", size="7"),
        rx.text(
            "Token is valid? ",
            rx.cond(TurnstileState.token_is_valid, "Yes ✓", "No ✗"),
            weight="bold",
        ),
        rx.cond(
            rx.State.is_hydrated & ~TurnstileState.token_is_valid,
            turnstile(),
        ),
        rx.cond(
            TurnstileState.token_is_valid,
            rx.text("Verification successful!", color="green", weight="bold"),
        ),
        height="100vh",
        align="center",
        justify="center",
        spacing="4",
        p="4",
    )


app = rx.App()
app.add_page(index, title="Simple Turnstile Demo", on_load=TurnstileState.reset_validation)
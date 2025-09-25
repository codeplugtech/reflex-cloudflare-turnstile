# cloudflare-turnstile

A reflex-cloudflare-turnstile component for [Reflex](https://reflex.dev) applications. Built on top of react-turnstile, it provides a smart verification with minimal user interaction.


## 📦 Installation

```bash
pip install reflex-cloudflare-turnstil
```

## 🚀 Quick Start

```python
import reflex as rx

import reflex_cloudflare_turnstile
from reflex_cloudflare_turnstile import turnstile, TurnstileState


if not reflex_cloudflare_turnstile.is_key_set():
    reflex_cloudflare_turnstile.set_site_key(" ") # Get test site key from cloudflare website
    reflex_cloudflare_turnstile.set_secret_key(" ") # Get test secret key from cloudflare website


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


```

<img src="https://cdn.pixalto.app/reflex-cloudflare-turnstile-demo.png">

Don't forget to add the frontend package to your `rxconfig.py`:

```python
import reflex as rx

config = rx.Config(
    app_name="cloudflare_turnstile_demo",
    frontend_packages=[
        "@marsidev/react-turnstile" 
    ]
)
```

## 📝 Changelog

### v0.0.1 (2025-25-09)
- Initial release
- Basic cloudflare turnstile functionality

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check the [GitHub Issues](https://github.com/codeplugtech/reflex-cloudflare-turnstile/issues)
2. Join the [Reflex Discord](https://discord.com/channels/1029853095527727165) community
3. Create a new issue with detailed information


## 🙏 Acknowledgments

- Built with [Reflex](https://github.com/reflex-dev/reflex) - The web framework for Python
- Powered by [react-turnstile](https://docs.page/marsidev/react-turnstile) - React cloudflare turnstile component

---

**Made with ❤️ for the Reflex community**

*Star ⭐ this repo if you find it useful!*

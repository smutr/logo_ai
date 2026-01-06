from . import start, call_start_generate, call_help, call_back, call_gallery, call_profile, call_buy_credits

routers = [
    start.router,
    call_start_generate.router,
    call_help.router,
    call_back.router,
    call_gallery.router,
    call_profile.router,
    call_buy_credits.router
]
from . import start, call_start_generate, call_help, call_back

routers = [
    start.router,
    call_start_generate.router,
    call_help.router,
    call_back.router
]
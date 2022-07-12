from .users import OnlyAdminFilter


def setup_filters(dp):
    dp.bind_filter(OnlyAdminFilter)
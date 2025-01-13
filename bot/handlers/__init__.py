from .commands import commands
from .main_menu import main_menu
from .channel_actions import ch_actions
from .givaway_actions import giv_actions
from .lot_actions import lot_actions


routers = [
    commands, 
    main_menu,
    giv_actions,
    ch_actions,
    lot_actions
]


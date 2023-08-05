
import functools
from typing import TYPE_CHECKING, TypeVar, Generic
from xoa_driver.internals.core.commands import enums
from xoa_driver.internals.core.commands import (
    M_MODEL, 
    M_PORTCOUNT,
    M_RESERVATION,
    M_RESERVEDBY, 
    M_SERIALNO, 
    M_VERSIONNO
)
from xoa_driver.internals.core.transporter import funcs
from xoa_driver.internals.utils import attributes as utils

if TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf
    from . import __interfaces as m_itf

from xoa_driver.internals.state_storage import modules_state

T = TypeVar('T', bound="modules_state.ModuleLocalState")
class BaseModule(Generic[T]):
    
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        self._conn = conn
        self.module_id = init_data.module_id
        self.ports_count = init_data.ports_count
        self.reservation = M_RESERVATION(self._conn, self.module_id)
        self.reserved_by = M_RESERVEDBY(self._conn, self.module_id)
        self.model = M_MODEL(self._conn, self.module_id)
        self.serial_number = M_SERIALNO(self._conn, self.module_id)
        self.version_number = M_VERSIONNO(self._conn, self.module_id)
        self.port_count = M_PORTCOUNT(self._conn, self.module_id)
        
        self._local_states: T = modules_state.ModuleLocalState()
        
        self._register_subscriptions()
    
    @property
    def info(self) -> T:
        """Module info"""
        return self._local_states  # type: ignore

    def __await__(self):
        return self._setup().__await__()

    async def _setup(self):
        (
            reservation_r,
            reserved_by_r,
            model_r,
        ) = await funcs.apply(
            self.reservation.get(),
            self.reserved_by.get(),
            self.model.get(),
        )
        self._local_states.reservation = reservation_r.operation
        self._local_states.reserved_by = reserved_by_r.username
        self._local_states.model = model_r.model
        return self

    def _check_identity(self, request) -> bool:
        return self.module_id == request.header.module_index
    
    def _register_subscriptions(self) -> None:
        self._conn.subscribe(M_RESERVEDBY, utils.Update(self._local_states, "reserved_by", "username", self._check_identity))
        self._conn.subscribe(M_RESERVATION, utils.Update(self._local_states, "reservation", "operation", self._check_identity))
        self._conn.subscribe(M_MODEL, utils.Update(self._local_states, "model", "model", self._check_identity))
    
    def __is_reservation(self, reserved_status: enums.ReservedStatus) -> bool:
        return self._local_states.reservation == reserved_status

    is_released = functools.partialmethod(__is_reservation, enums.ReservedStatus.RELEASED)
    is_reserved_by_me = functools.partialmethod(__is_reservation, enums.ReservedStatus.RESERVED_BY_YOU)

    on_reservation_change = functools.partialmethod(utils.on_event, M_RESERVATION)
    on_reserved_by_change = functools.partialmethod(utils.on_event, M_RESERVEDBY)
    on_model_change = functools.partialmethod(utils.on_event, M_MODEL)
    on_serial_number_change = functools.partialmethod(utils.on_event, M_SERIALNO)
    on_version_number_change = functools.partialmethod(utils.on_event, M_VERSIONNO)
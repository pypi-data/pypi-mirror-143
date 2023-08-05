import functools
from typing import TYPE_CHECKING
from xoa_driver.internals.ports import base_port

from xoa_driver.internals.core.commands import (
    P_RECEIVESYNC,
    P4_TRAFFIC,
    P4_STATE,
    P4_CAPABILITIES,
    P4_STATE_STATUS,
    P4_VLAN_OFFLOAD,
    P4_ARP_CONFIG,
    P4_NDP_CONFIG,
    P4_CAPTURE,
    P4_CAPTURE_GET_FIRST,
    P4_CAPTURE_GET_NEXT,
    P4_TX_PACKET_SIZE,
    P4_RX_PACKET_SIZE,
    P4_TX_MTU,
    P4_RX_MTU,
    P4_CLEAR,
    P4_SPEEDSELECTION,
    P4_MAX_PACKET_RATE,
    P4_PCI_INFO,
    P4_FW_VER,
    P4_DEV_NAME,
    P4_PORT_TYPE,
    P4_LICENSE_INFO,
    P4_APTITUDES,
)

if TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf

from xoa_driver.internals.core.transporter import funcs
from xoa_driver.internals.state_storage import ports_state
from xoa_driver.internals.utils import attributes as utils
from xoa_driver.internals.utils.indices import index_manager as im
from xoa_driver.internals.indices.connection_group.cg import ConnectionGroupIdx

from .counters import PCounters
from .packet_engine import PacketEngine

class PCapture:
    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        self.start = P4_CAPTURE(conn, module_id, port_id)
        self.get_first_frame = P4_CAPTURE_GET_FIRST(conn, module_id, port_id)
        self.get_next_frame = P4_CAPTURE_GET_NEXT(conn, module_id, port_id)



class PortL47(base_port.BasePort["ports_state.PortL47LocalState"]):
    """Port L47"""
    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        super().__init__(conn, module_id, port_id)
        self.sync_status = P_RECEIVESYNC(conn, module_id, port_id)
        
        self.traffic = P4_TRAFFIC(self._conn, module_id, port_id)
        self.clear = P4_CLEAR(self._conn, module_id, port_id)
        self.state = P4_STATE(self._conn, module_id, port_id)
        self.type = P4_PORT_TYPE(self._conn, module_id, port_id)
        self.aptitudes = P4_APTITUDES(self._conn, module_id, port_id)
        self.last_state_status = P4_STATE_STATUS(self._conn, module_id, port_id)
        
        self.nic_name = P4_DEV_NAME(self._conn, module_id, port_id)
        self.nic_firmware_version = P4_FW_VER(self._conn, module_id, port_id)
        self.vlan_offload = P4_VLAN_OFFLOAD(self._conn, module_id, port_id)
        
        self.max_packet_rate = P4_MAX_PACKET_RATE(self._conn, module_id, port_id)
        self.capabilities = P4_CAPABILITIES(self._conn, module_id, port_id)
        self.speed_selection = P4_SPEEDSELECTION(self._conn, module_id, port_id)
        
        # region Not sure if this commands must be atthis level
        self.tx_packet_size = P4_TX_PACKET_SIZE(self._conn, module_id, port_id)
        self.rx_packet_size = P4_RX_PACKET_SIZE(self._conn, module_id, port_id)
        self.tx_mtu = P4_TX_MTU(self._conn, module_id, port_id)
        self.rx_mtu = P4_RX_MTU(self._conn, module_id, port_id)
        # endregion
        
        self.pci_info = P4_PCI_INFO(self._conn, module_id, port_id)
        self.license_info = P4_LICENSE_INFO(self._conn, module_id, port_id)
        
        self.arp_config = P4_ARP_CONFIG(self._conn, module_id, port_id)
        self.ndp_config = P4_NDP_CONFIG(self._conn, module_id, port_id)
        
        self.capture = PCapture(self._conn, module_id, port_id)
        self.counters = PCounters(self._conn, module_id, port_id)
        self.packet_engine = PacketEngine(self._conn, module_id, port_id)
        
        self.local_states = ports_state.PortL47LocalState()
        
        self.conection_groups: "im.IndexManager[ConnectionGroupIdx]" = im.IndexManager(
            self._conn, 
            ConnectionGroupIdx, 
            module_id, 
            port_id
        )
    
    async def _setup(self):
        await super()._setup()
        (
            sync_status_r,
            traffic_state_r,
            capabilities_r
        ) = await funcs.apply(
            self.sync_status.get(),
            self.state.get(),
            self.capabilities.get(),
        )
        self.local_states.capabilities = capabilities_r
        self.local_states.sync_status = sync_status_r.sync_status
        self.local_states.traffic_state = traffic_state_r.state
        return self

    def _register_subscriptions(self) -> None:
        super()._register_subscriptions()
        self._conn.subscribe(P_RECEIVESYNC, utils.Update(self.local_states, "sync_status", "sync_status", self._check_identity))
        self._conn.subscribe(P4_STATE, utils.Update(self.local_states, "traffic_state", "on_off", self._check_identity))
    
    on_receave_sync_change = functools.partialmethod(utils.on_event, P_RECEIVESYNC)
    on_capabilities_change = functools.partialmethod(utils.on_event, P4_CAPABILITIES)
    on_speed_selection_change = functools.partialmethod(utils.on_event, P4_SPEEDSELECTION)
    on_state_change = functools.partialmethod(utils.on_event, P4_STATE)
    on_license_info_change = functools.partialmethod(utils.on_event, P4_LICENSE_INFO)

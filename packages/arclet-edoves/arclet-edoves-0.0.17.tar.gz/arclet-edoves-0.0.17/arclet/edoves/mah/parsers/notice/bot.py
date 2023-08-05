from typing import cast

from arclet.edoves.builtin.medium import DictMedium, Notice
from arclet.edoves.main.parser import BaseDataParser, ParserBehavior, ParserMetadata
from arclet.edoves.main.utilles import IOStatus
from ...monomers import MahEntity
from ...protocol import MAHProtocol


class BotBaseNoticeMeta(ParserMetadata):
    parser_targets = [
        "BotOnlineEvent",
        "BotOfflineEventActive",
        "BotOfflineEventForce",
        "BotOfflineEventDropped",
        "BotReloginEvent"
    ]


class BotStatusMeta(ParserMetadata):
    parser_targets = [
        "BotGroupPermissionChangeEvent",
        "BotMuteEvent",
        "BotUnmuteEvent"
    ]


class BotRelationshipMeta(ParserMetadata):
    parser_targets = [
        "BotJoinGroupEvent",
        "BotLeaveEventActive",
        "BotLeaveEventKick",
        "RelationshipRemove"

    ]


class BotNoticeMeBehavior(ParserBehavior):
    async def from_docker(self, protocol: MAHProtocol, data: DictMedium):
        notice = Notice().create(protocol.current_scene.protagonist, {}, self.io.metadata.select_type)
        await protocol.screen.push_medium(notice)
        await protocol.screen.broadcast_medium("NoticeMe")

    async def to_docker(self, protocol: MAHProtocol, data: DictMedium):
        pass


class BotStatusUpdateBehavior(ParserBehavior):
    async def from_docker(self, protocol: MAHProtocol, data: DictMedium):
        ev_type = self.io.metadata.select_type
        if ev_type == "BotGroupPermissionChangeEvent":
            group = protocol.include_monomer("group", data.content.pop('group'))
            protocol.current_scene.protagonist.metadata.group_id = group.metadata.pure_id
            notice = Notice().create(protocol.current_scene.protagonist, data.content, ev_type)
            await protocol.screen.push_medium(notice)
            await protocol.screen.broadcast_medium("MonomerStatusUpdate")
        elif ev_type in ("BotMuteEvent", "BotUnmuteEvent"):
            operator_data = data.content.pop('operator')
            operator = protocol.include_monomer("member", operator_data)
            group = protocol.include_monomer("group", operator_data['group'])
            if not group.get_child(operator.metadata.pure_id):
                group.set_child(operator)
            operator.metadata.group_id = group.metadata.pure_id
            notice = Notice().create(protocol.current_scene.protagonist, data.content, ev_type)
            notice.operator = operator
            await protocol.screen.push_medium(notice)
            await protocol.screen.broadcast_medium(
                "MonomerStatusUpdate", action="set" + ev_type.replace('Bot', '').replace('Event', '')
            )

    async def to_docker(self, protocol: MAHProtocol, data: DictMedium):
        pass


class BotRelationshipOperateBehavior(ParserBehavior):

    async def from_docker(self, protocol: MAHProtocol, data: DictMedium):
        ev_type = self.io.metadata.select_type
        if ev_type == "BotJoinGroupEvent":
            group = protocol.include_monomer("group", data.content.pop('group'))
            protocol.current_scene.protagonist.metadata.group_id = group.metadata.pure_id
            notice = Notice().create(protocol.current_scene.protagonist, data.content, ev_type)
            await protocol.screen.push_medium(notice)
            await protocol.screen.broadcast_medium(
                "RelationshipSetup", relationship="Group"
            )
        elif ev_type == "BotLeaveEventActive":
            group = protocol.exclude_monomer("group", data.content.pop('group'))
            notice = Notice().create(protocol.current_scene.protagonist, {"group": group}, ev_type)
            await protocol.screen.push_medium(notice)
            await protocol.screen.broadcast_medium(
                "RelationshipTerminate", relationship="Group"
            )
        elif ev_type == "BotLeaveEventKick":
            group = protocol.exclude_monomer("group", data.content.pop('group'))
            operator = protocol.exclude_monomer(
                "member", data.content.pop('operator'), group_id=group.metadata.pure_id
            )
            operator.metadata.group_id = group.metadata.pure_id
            notice = Notice().create(protocol.current_scene.protagonist, {"group": group}, ev_type)
            notice.operator = operator
            await protocol.screen.push_medium(notice)
            await protocol.screen.broadcast_medium(
                "RelationshipSevered", relationship="Group"
            )

    async def to_docker(self, protocol: MAHProtocol, data: DictMedium):
        target = cast(MahEntity, data.content.get("target"))
        relationship = data.content.get("relationship")
        if relationship == "Friend":
            # 删除好友
            protocol.current_scene.protagonist.relation['children'].remove(target.metadata.identifier)
            if not target.compare("Member"):
                # 解除所有关系
                protocol.current_scene.monomers.remove(target.metadata.pure_id)
                target.metadata.state = IOStatus.DELETE_WAIT
            else:
                target.remove_tags("Friend")  # 删除好友标签
            await protocol.docker.behavior.session_handle(
                "post",
                "deletaFriend",
                {
                    "sessionKey": protocol.docker.metadata.session_keys[protocol.current_scene.scene_name],
                    "target": target.metadata.identifier,
                }
            )
        if relationship == "Group":
            protocol.current_scene.protagonist.parents.pop(target.metadata.identifier)  # 群组与bot的关系解除
            for mo in target.children.values():
                mo.parents.pop(target.metadata.identifier)  # 群组与群组成员的关系解除
                if len(mo.parents) == 0:
                    protocol.current_scene.monomers.pop(mo.metadata.identifier)  # 群组成员与bot的所有关系解除
                elif mo.compare("Friend") and len(mo.parents) == 1:
                    mo.remove_tags("Member")  # 群组成员与bot的群友关系解除

            await protocol.docker.behavior.session_handle(
                "post",
                "quit",
                {
                    "sessionKey": protocol.docker.metadata.session_keys[protocol.current_scene.scene_name],
                    "target": target.metadata.identifier,
                }
            )


@MAHProtocol.register_parser
class BotBaseEventParser(BaseDataParser):
    prefab_metadata = BotBaseNoticeMeta
    prefab_behavior = BotNoticeMeBehavior


@MAHProtocol.register_parser
class BotStatusUpdateEventParser(BaseDataParser):
    prefab_metadata = BotStatusMeta
    prefab_behavior = BotStatusUpdateBehavior


@MAHProtocol.register_parser
class BotRelationshipEventParser(BaseDataParser):
    prefab_metadata = BotRelationshipMeta
    prefab_behavior = BotRelationshipOperateBehavior

